from fastapi import APIRouter


router = APIRouter()


@router.post("/create")
async def create_user():
    pass


@router.get("/get")
async def get_user():
    pass


@router.patch("/update")
async def update_user():
    pass


@router.delete("/delete")
async def delete_user():
    pass


