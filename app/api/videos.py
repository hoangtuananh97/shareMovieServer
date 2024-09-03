import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.websockets import websocketsManager
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.VideoResponse)
async def create_video(
        payload: schemas.VideoCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    new_video = models.Video(**payload.dict(), shared_by=current_user.id)
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    # Broadcast notification to all connected clients
    notification = {
        "type": "newVideo",
        "data": {
            "title": new_video.title,
            "description": new_video.description,
            "shared_by": current_user.email,
            "id": str(new_video.id),
        }
    }
    await websocketsManager.broadcast(json.dumps(notification))
    return schemas.VideoResponse(Status=schemas.Status.Success, Video=schemas.VideoSchema.from_orm(new_video))


@router.get("/{video_id}", response_model=schemas.VideoResponse)
def get_video(video_id: UUID, db: Session = Depends(get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No video with this id: {video_id} found")
    return schemas.VideoResponse(Status=schemas.Status.Success, Video=schemas.VideoSchema.from_orm(video))


@router.get("", response_model=schemas.ListVideoResponse)
def list_videos(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    videos = (
        db.query(models.Video)
        .join(models.User, models.Video.shared_by == models.User.id)
        .order_by(desc(models.Video.shared_at))
        .offset(skip).limit(limit).all()
    )
    video_response = []
    for video in videos:
        video_response.append(schemas.VideoListSchema.from_orm({
            "id": video.id,
            "title": video.title,
            "shared_by": video.user.email,
            "video_url": video.video_url,
            "image_url": video.image_url,
            "tags": video.tags,
            "likes": video.likes,
            "dislikes": video.dislikes,
            "shared_at": video.shared_at,
        }))
    return schemas.ListVideoResponse(Status=schemas.Status.Success, Videos=video_response)


@router.patch("/{video_id}", response_model=schemas.VideoResponse)
def update_video(
        video_id: UUID,
        payload: schemas.VideoUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    video_query = db.query(models.Video).filter(models.Video.id == video_id)
    video = video_query.first()
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No video with this id: {video_id} found")
    if video.shared_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this video")

    update_data = payload.dict(exclude_unset=True)
    video_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(video)
    return schemas.VideoResponse(Status=schemas.Status.Success, Video=schemas.VideoSchema.from_orm(video))


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(video_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    video_query = db.query(models.Video).filter(models.Video.id == video_id)
    video = video_query.first()
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No video with this id: {video_id} found")
    if video.shared_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this video")

    video_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "success"}
