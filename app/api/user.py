from datetime import timedelta, datetime

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
from app.auth import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_user, hash_password
from app.database import get_db

load_dotenv()

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()

    if user and not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user:
        hashed_password = hash_password(form_data.password)
        user_data = form_data.model_dump(exclude={'password'})
        user_data['password'] = hashed_password

        new_user = models.User(**user_data)
        db.add(new_user)
        db.commit()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "email": form_data.email, "token_type": "bearer"}


# Update the create_user function to use get_password_hash
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(payload: schemas.UserCreateSchema, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(payload.password)
        user_data = payload.model_dump(exclude={'password'})
        user_data['password'] = hashed_password

        new_user = models.User(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        user_response = schemas.UserResponseSchema.model_validate(new_user)
        return schemas.UserResponse(Status=schemas.Status.Success, User=user_response)
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user.",
        )


@router.get(
    "/{userId}", status_code=status.HTTP_200_OK, response_model=schemas.GetUserResponse
)
def get_user(userId: str, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == userId)
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with this id: `{userId}` found",
        )

    try:
        user_response = schemas.UserResponseSchema.model_validate(db_user)
        return schemas.GetUserResponse(Status=schemas.Status.Success, User=user_response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the user.",
        ) from e


@router.patch(
    "/{userId}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.UserResponse,
)
def update_user(
        userId: str, payload: schemas.UserUpdateSchema,
        db: Session = Depends(get_db),
        _: models.User = Depends(get_current_user)
):
    db_user = db.query(models.User).filter(models.User.id == userId).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with this id: `{userId}` found",
        )

    update_data = payload.model_dump(exclude_unset=True)

    # If password is being updated, hash it
    if 'password' in update_data:
        update_data['password'] = hash_password(update_data['password'])

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db_user.updatedAt = datetime.utcnow()
    try:
        db.commit()
        db.refresh(db_user)

        user_response = schemas.UserResponseSchema.model_validate(db_user)
        return schemas.UserResponse(Status=schemas.Status.Success, User=user_response)
    except IntegrityError as e:
        db.rollback()
        if "uq_user_email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the user.",
        )


@router.delete(
    "/{userId}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.DeleteUserResponse,
)
def delete_user(userId: str, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    try:
        user_query = db.query(models.User).filter(models.User.id == userId)
        user = user_query.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No User with this id: `{userId}` found",
            )
        user_query.delete(synchronize_session=False)
        db.commit()
        return schemas.DeleteUserResponse(
            Status=schemas.Status.Success, Message="User deleted successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user.",
        ) from e


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=schemas.ListUserResponse
)
def get_users(
        db: Session = Depends(get_db),
        _: models.User = Depends(get_current_user),
        limit: int = 10, page: int = 1, search: str = ""
):
    skip = (page - 1) * limit

    users = (
        db.query(models.User)
        .filter(models.User.email.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return schemas.ListUserResponse(
        status=schemas.Status.Success, results=len(users),
        users=[schemas.UserResponseSchema.model_validate(user) for user in users]
    )

