from fastapi import FastAPI
import models
from database import engin
from routers import auth, todos


app = FastAPI()

models.Base.metadata.create_all(bind=engin)

# defining auth.router to include it in our FastAPI
app.include_router(auth.router)

# defining todos.router to include it in our FastAPI
app.include_router(todos.router)
