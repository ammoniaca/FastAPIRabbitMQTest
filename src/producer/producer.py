import asyncio
import json
from aio_pika import connect_robust, Message, DeliveryMode, exceptions
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from src.config import settings
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

SECONDS_WAIT: int = 5
MAX_RETRIES = 30  # massimo tentativi

async def safe_declare_queue(channel: AbstractChannel, queue_name: str, durable=True):
    """
    Safely declares a RabbitMQ queue.

    Declares a queue safely. If the queue exists with different parameters, raises an error.

    This function attempts to declare a queue with the given name and durability.
    If the queue already exists with the same parameters, it will succeed silently.
    If the queue exists with different parameters, an exception is raised.

    Parameters
    ----------
    channel : AbstractChannel
        The RabbitMQ channel to use for declaring the queue.
    queue_name : str
        The name of the queue to declare.
    durable : bool, optional
        Whether the queue should survive broker restarts. Defaults to True.

    Raises
    ------
    exceptions.ChannelClosed
        If the queue exists with different parameters or if there is a channel error.
    """
    try:
        await channel.declare_queue(queue_name, durable=durable)
        logging.info(f"Queue '{queue_name}' declared successfully or already exists.")
    except exceptions.ChannelClosed as e:
        logging.error(f"Cannot declare queue '{queue_name}': {e}")
        raise


# Function to connect to RabbitMQ
async def get_rabbitmq_connection(queue_name: str) -> tuple[AbstractRobustConnection, AbstractChannel]:
    """
    Establishes a robust asynchronous connection to a RabbitMQ server and declares a durable queue.

    This function will attempt to connect to RabbitMQ repeatedly until successful or until
    the maximum number of retries is reached. It is designed to be async-friendly for
    integration with FastAPI or other asynchronous frameworks.

    Parameters
    ----------
    queue_name : str
        The name of the RabbitMQ queue to declare and use for publishing messages.

    Returns
    -------
    tuple[AbstractRobustConnection, AbstractChannel]
        A tuple containing:
        - `connection`: the established aio-pika robust connection to RabbitMQ.
        - `channel`: the channel on which messages can be published.

    Raises
    ------
    ConnectionError
        If the connection could not be established after the maximum number of retries.

    Notes
    -----
    - The function uses `MAX_RETRIES` and `SECONDS_WAIT` for retry logic.
    - Uses `aio_pika.connect_robust` to ensure the connection automatically recovers from network failures.
    - The queue is declared as durable to persist messages in RabbitMQ even if the server restarts.
    """
    retries = 0
    while retries < MAX_RETRIES:
        try:
            connection: AbstractRobustConnection = await connect_robust(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_AMQP_PORT,
            )
            channel: AbstractChannel = await connection.channel()
            # await channel.declare_queue(QUEUE_NAME, durable=True)
            await safe_declare_queue(channel, queue_name, durable=True) # Safely declares a RabbitMQ queue
            logging.info("RabbitMQ connected!")
            return connection, channel
        except exceptions.AMQPConnectionError:
            retries += 1
            logging.warning(
                f"RabbitMQ not ready, retrying in {SECONDS_WAIT} seconds... ({retries}/{MAX_RETRIES})"
            )
            await asyncio.sleep(SECONDS_WAIT)

    logging.error(f"Could not connect to RabbitMQ after {MAX_RETRIES} retries")
    raise ConnectionError(f"Could not connect to RabbitMQ after {MAX_RETRIES} retries")

async def send_message_to_rabbitmq(channel: AbstractChannel, queue_name: str, message: dict):
    """
    Sends a JSON message to a specified RabbitMQ queue.

    The message is published to the default exchange with persistent delivery,
    ensuring it is not lost if RabbitMQ restarts.

    Parameters
    ----------
    channel : AbstractChannel
        The RabbitMQ channel to use for publishing the message.
    queue_name : str
        The name of the queue to which the message will be sent.
    message : dict
        The message payload to send. It will be serialized to JSON.

    Raises
    ------
    Exception
        Any exceptions raised by the publish operation (e.g., connection errors) will propagate.
    """
    await channel.default_exchange.publish(
        Message(
            body=json.dumps(message).encode(),
            delivery_mode=DeliveryMode.PERSISTENT
        ),
        routing_key=queue_name
    )
    logging.info(f"Message sent: {message}")