from fastapi import FastAPI, Depends
import models
from database import engin
from routers import auth, todos, users
from company import companyapis, dependencies


app = FastAPI()

models.Base.metadata.create_all(bind=engin)

# defining auth.router to include it in our FastAPI
app.include_router(auth.router)

# defining todos.router to include it in our FastAPI
app.include_router(todos.router)

app.include_router(users.router)


# externally configuring prefix, tags, and responses
# in main.py
# before calling a companyapi there specific security
# that gotta be matched. in that case, we can define a dependency
# that checks token_header before calling the api.
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {"description": "Internal use only"}}
)