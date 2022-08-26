from fastapi import FastAPI

app = FastAPI()


MEMBERS = {
    "Member_1": {"first_name": "Alireza", "last_name": "Bodaghi"},
    "Member_2": {"first_name": "Amir", "last_name": "Jafari"},
    "Member_3": {"first_name": "Ramtin", "last_name": "Sahraee"},
    "Member_4": {"first_name": "Hossein", "last_name": "Qorbannezhad"}
}


@app.post("/")
async def create_member(first_name: str, last_name: str):
    max_member = 0
    if len(MEMBERS) > 0:
        for key in MEMBERS:
            current_key_num = int(key.split("_")[-1])
            if max_member < current_key_num:
                max_member = current_key_num
    MEMBERS[f"Member_{max_member + 1}"] = {"first_name":first_name, "last_name": last_name}
    return MEMBERS[f"Member_{max_member + 1}"]