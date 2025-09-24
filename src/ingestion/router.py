from fastapi import APIRouter
from src.ingestion.schemas import Items

router = APIRouter(
    prefix="/parameters",
    tags=["Data ingestion"]
)

@router.post("/")
async def post(items: Items):
    print(items)
    pass