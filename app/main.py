from app import models
from app.api import user, videos, uploads, websockets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(uploads.router, prefix="/api/uploads", tags=["uploads"])
app.include_router(websockets.router, prefix="/ws", tags=["websocket"])


@app.get("/api/healthchecker")
def root():
    return {"message": "The API is LIVE!!"}
