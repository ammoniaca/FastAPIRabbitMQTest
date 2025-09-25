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
        Can only be started once. Further POST requests will return 400.
    """
    try:
        # check if the task has already started
        if getattr(app_request.app.state, "periodic_task", None) is not None:
            logging.warning("Periodic sender already running, rejecting new POST")
            raise HTTPException(status_code=400, detail="Periodic sender already running")

        # create and save the task in the app status
        channel = app_request.app.state.rabbit_channel
        task = asyncio.create_task(
            periodic_sender(
                channel=channel,
                process_name=request.process_name,
                min_len=request.range.min,
                max_len=request.range.max)
        )
        app_request.app.state.periodic_task = task
        return {"status": "scheduled", "process": request.process_name}
    except HTTPException:
        raise  # relaunch without overwriting the detail
    except Exception as e:
        logging.error(f"Error scheduling periodic sender: {e}")
        raise HTTPException(status_code=500, detail="Could not schedule periodic sender")
