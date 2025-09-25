import asyncio
from datetime import datetime, timezone
from src.producer.random_string_generator import random_string_generator
from src.producer.schemas import PayloadModel
from src.config import settings
from src.producer.producer import send_message_to_rabbitmq
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

WAIT_TIME = 10

async def periodic_sender(channel, process_name: str, min_len: int, max_len: int):
    """
    Periodically sends a message to RabbitMQ.

    Sends the first message immediately, then continues sending messages
    at fixed intervals defined in ``settings.periodic_interval``.

    Parameters
    ----------
    channel : aio_pika.Channel
        The RabbitMQ channel used to publish messages.
    process_name : str
        Identifier of the process sending the message.
    min_len : int
        Minimum length of the generated random string.
    max_len : int
        Maximum length of the generated random string.

    Notes
    -----
    - The loop runs indefinitely until the application shuts down
      or the task is cancelled.
    - The interval duration is controlled by ``settings.periodic_interval``.
    - Each message includes a timestamp (UTC) in the ``created_at`` field.

    Raises
    ------
    Exception
        If there is an error while generating or sending the message.

    """
    try:
        while True:
            random_string = random_string_generator(min_length=min_len, max_length=max_len)
            payload = PayloadModel(
                queue_name=settings.queue_name,
                process_name=process_name,
                random_string=random_string,
                created_at=datetime.now(timezone.utc)
            )
            await send_message_to_rabbitmq(
                channel=channel,
                queue_name=settings.queue_name,
                message=payload.model_dump(mode="json")
            )
            logging.info(f"Message sent periodically: {payload.model_dump()}")
            await asyncio.sleep(WAIT_TIME)  # wait for a certain period of time
    except Exception as e:
        logging.error(f"Error in periodic sender: {e}")