from fastapi import FastAPI
from src.ingestion.router import router as controller_router
from src.rabbitmq.router import router as rabbitmq_router
from src.config import settings
from src.producer.producer import get_rabbitmq_connection
import logging
from contextlib import asynccontextmanager

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@asynccontextmanager
async def lifespan_handler(fastapi_app: FastAPI):
    # Startup: connect to RabbitMQ
    fastapi_app.state.rabbit_connection, fastapi_app.state.rabbit_channel = await get_rabbitmq_connection(settings.queue_name)
    logging.info("RabbitMQ connection established")
    yield
    # Shutdown: close connection
    await fastapi_app.state.rabbit_connection.close()
    logging.info("RabbitMQ connection closed")

app = FastAPI(
    title=settings.app_title,
    lifespan=lifespan_handler
)

app.include_router(controller_router)
app.include_router(rabbitmq_router)


