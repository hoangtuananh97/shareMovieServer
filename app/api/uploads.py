from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.auth import get_current_user
from app.models import User
from app.utils.s3 import upload_file_to_s3

router = APIRouter()


@router.post("/video")
async def upload_video(file: UploadFile = File(...), _: User = Depends(get_current_user)):
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.wmv')):
        raise HTTPException(status_code=400, detail="Invalid video file format")

    s3_url = upload_file_to_s3(file, "videos")
    return {"message": "Video uploaded successfully", "url": s3_url}


@router.post("/image")
async def upload_image(file: UploadFile = File(...), _: User = Depends(get_current_user)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        raise HTTPException(status_code=400, detail="Invalid image file format")

    s3_url = upload_file_to_s3(file, "images")
    return {"message": "Image uploaded successfully", "url": s3_url}
