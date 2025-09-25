import asyncio
from fastapi import APIRouter, Request, HTTPException
from src.ingestion.schemas import RequestModel
from src.producer.tasks import periodic_sender
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
        Starts sending messages to RabbitMQ every n seconds.
    """
    try:
        channel = app_request.app.state.rabbit_channel
        asyncio.create_task(periodic_sender(
            channel=channel,
            process_name=request.process_name,
            min_len=request.range.min,
            max_len=request.range.max)
        )
        return {"status": "scheduled"}
    except Exception as e:
        logging.error(f"Error scheduling periodic sender: {e}")
        raise HTTPException(status_code=500, detail="Could not schedule periodic sender")

    # try:
    #     random_string = random_string_generator(min_length=request.range.min, max_length=request.range.max)
    #     # generate message to rabbitmq
    #     payload = PayloadModel(
    #         queue_name=settings.queue_name,
    #         process_name=request.process_name,
    #         random_string=random_string,
    #         created_at=datetime.now(timezone.utc)
    #     )
    #     channel = app_request.app.state.rabbit_channel
    #     await send_message_to_rabbitmq(
    #         channel=channel,
    #         queue_name=settings.queue_name,
    #         message=payload.model_dump(mode="json")
    #     )
    #     logging.info(f"Message sent: {payload.model_dump()}")
    #     return {"status": "sent", "message": 124}
    # except Exception as e:
    #     logging.error(f"Error sending message: {e}")
    #     raise HTTPException(status_code=500, detail="Could not send message to RabbitMQ")