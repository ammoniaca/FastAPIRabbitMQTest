from fastapi import FastAPI
from src.ingestion.router import router as controller_router
from src.rabbitmq.router import router as rabbitmq_router
from src.config import settings

app = FastAPI(
    title=settings.app_title,
)

app.include_router(controller_router)
app.include_router(rabbitmq_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
