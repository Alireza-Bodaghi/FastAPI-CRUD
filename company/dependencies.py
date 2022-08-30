from fastapi import Header, HTTPException


INTERNAL_TOKEN = "ALLOWED"


# creating an internal token
async def get_token_header(internal_token: str = Header(...)):
    if internal_token != INTERNAL_TOKEN:
        raise HTTPException(status_code=400,
                            detail="Internal-Token header invalid")
