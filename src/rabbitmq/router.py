from fastapi import APIRouter
import httpx
import os


router = APIRouter(
    prefix="/rabbitmq",
    tags=["queues"]
)

RABBITMQ_API = os.getenv("RABBITMQ_API", "http://rabbitmq:15672/api/queues")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "secret")

@router.get("/queues")
def list_queues():
    try:
        response = httpx.get(RABBITMQ_API, auth=(RABBITMQ_USER, RABBITMQ_PASS))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}