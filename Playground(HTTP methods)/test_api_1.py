from typing import Union, Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def first_api():
    return {"message": "HelloWorld!"}


MEMBERS = {
    "Member_1": {"first_name": "Alireza", "last_name": "Bodaghi"},
    "Member_2": {"first_name": "Amir", "last_name": "Jafari"},
    "Member_3": {"first_name": "Ramtin", "last_name": "Sahraee"},
    "Member_4": {"first_name": "Hossein", "last_name": "Qorbannezhad"}
}


@app.get("/members")
async def read_all_members():
    return MEMBERS


# Optional Query Parameters
# there are three ways to make an Optional Query Parameter:
# 1. Using Optional module like -> p: Optional[str] = None
# 2. Using Union module like -> p: Union[str, None] = None in python 3.9 and further
# 3. in python 3.10, you can just declare like -> p: str | None = None
@app.get("/skip_member")
async def skip_name(skip_member_name: Union[str, None] = None):
    if skip_member_name is not None:
        new_member = MEMBERS.copy()
        del new_member[skip_member_name]
        return new_member
    return MEMBERS


# remember!
# order matters in path parameters, so you MUST
# always declare same-fixed paths before those which
# have variables as an arguments. otherwise it will
# categorized under the ones getting input/variables in path as an argument.
@app.get("/members/myfriend")
async def read_member():
    return {"member_name": "Hossein Qorbannezhad"}


# echo!
@app.get("/members/{member_name}")
async def read_member(member_name):
    return {"member_name": member_name}


# echo! using python type (Integer)
@app.get("/members/{member_id}")
async def read_member(member_id: int):
    return {"member_id": member_id}


# getting member name from dict
@app.get("/{member_num}")
async def read_member_name(member_num: str):
    return MEMBERS[member_num]
