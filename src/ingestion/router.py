from fastapi import APIRouter, Request, HTTPException
from datetime import datetime, timezone
from src.ingestion.schemas import RequestModel
from src.config import settings
from src.producer.producer import send_message_to_rabbitmq
from src.producer.schemas import PayloadModel
from src.producer.random_string_generator import random_string_generator
import logging


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


router = APIRouter(
    prefix="/parameters",
    tags=["Data ingestion"]
)


@router.post("/")
async def post(request: RequestModel, app_request: Request):
    """
    Receives a number via POST and sends it to RabbitMQ.
    """
    try:
        random_string = random_string_generator(min_length=request.range.min, max_length=request.range.max)
        # generate message to rabbitmq
        payload = PayloadModel(
            queue_name=request.queue_name,
            process_tag=request.process_tag,
            random_string=random_string,
            created_at=datetime.now(timezone.utc)
        )
        channel = app_request.app.state.rabbit_channel
        await send_message_to_rabbitmq(
            channel=channel,
            queue_name=settings.QUEUE_NAME,
            message=payload.model_dump()
        )
        logging.info(f"Message sent: {payload.model_dump()}")
        return {"status": "sent", "number": 12}
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail="Could not send message to RabbitMQ")