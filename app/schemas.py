from enum import Enum
from datetime import datetime
from typing import List, Optional

from decouple import config
from pydantic import BaseModel, Field, EmailStr, field_serializer
from uuid import UUID


class UserBaseSchema(BaseModel):
    email: EmailStr = Field(..., description="The email of the user", example="test@gmail.com")

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., description="The password of the user", example="password", min_length=8)


class UserLoginSchema(UserBaseSchema):
    password: str = Field(..., description="The password of the user", example="password", min_length=8)


class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserResponseSchema(UserBaseSchema):
    id: UUID


class Status(Enum):
    Success = "Success"
    Failed = "Failed"


class UserResponse(BaseModel):
    Status: Status
    User: UserResponseSchema


class GetUserResponse(BaseModel):
    Status: Status
    User: UserResponseSchema


class ListUserResponse(BaseModel):
    status: Status
    results: int
    users: List[UserResponseSchema]


class DeleteUserResponse(BaseModel):
    Status: Status
    Message: str


class Token(BaseModel):
    access_token: str
    token_type: str
    email: str | None = None


class TokenData(BaseModel):
    email: str | None = None


class UserResponseVideoSchema(BaseModel):
    id: UUID
    email: EmailStr | None = None


class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: str
    image_url: str
    tags: Optional[str] = None


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    title: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None


class VideoSchema(VideoBase):
    id: UUID
    shared_by: UUID
    likes: int
    dislikes: int
    shared_at: datetime

    class Config:
        from_attributes = True

    @field_serializer("video_url")
    def serialize_video_url(self, video_url: str, _info):
        return f"https://{config('S3_BUCKET')}.s3.{config('AWS_REGION')}.amazonaws.com/{video_url}"

    @field_serializer("image_url")
    def serialize_image_url(self, image_url: str, _info):
        return f"https://{config('S3_BUCKET')}.s3.{config('AWS_REGION')}.amazonaws.com/{image_url}"


class VideoListSchema(VideoSchema):
    shared_by: str


class VideoResponse(BaseModel):
    Status: Status
    Video: VideoSchema


class ListVideoResponse(BaseModel):
    Status: Status
    Videos: List[VideoListSchema]
