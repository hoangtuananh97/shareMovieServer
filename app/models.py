import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from app.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary key and GUID type
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, index=True, unique=True)
    password = Column(String(255), nullable=False)
    videos = relationship("Video", back_populates="user")


class Video(Base):
    __tablename__ = "videos"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    video_url = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=False)
    tags = Column(String(255), nullable=True)
    shared_by = Column(UUIDType(binary=False), ForeignKey('users.id'), nullable=False)
    likes = Column(Integer, nullable=False, default=0)
    dislikes = Column(Integer, nullable=False, default=0)
    shared_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    user = relationship("User", back_populates="videos")