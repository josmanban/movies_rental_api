from fastapi import APIRouter

router = APIRouter()


@router.get("/movies", tags=["movies"])
async def list():
    return {"movies": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
