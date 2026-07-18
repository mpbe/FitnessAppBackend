from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, workouts
from fastapi.middleware.cors import CORSMiddleware
from app.config import config
from fastapi.responses import RedirectResponse

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create database tables
    Base.metadata.create_all(bind=engine)
    yield

origins = [
    config.FRONTEND_URL
]

#add CORS middleware to help integration with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#register the routers when created
app.include_router(users.router)
app.include_router(workouts.router)


@app.get("/", include_in_schema=False)
def homepage():
    return RedirectResponse("/docs")