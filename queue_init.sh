#!/bin/sh

# aspetta RabbitMQ pronto
while ! rabbitmqctl status >/dev/null 2>&1; do
    echo "Waiting RabbitMQ..."
    sleep 2
done

echo "Creazione coda: $QUEUE_NAME"

rabbitmqadmin declare queue name="$QUEUE_NAME" durable=true \
  -u "$RABBITMQ_DEFAULT_USER" -p "$RABBITMQ_DEFAULT_PASS" -V "$RABBITMQ_DEFAULT_VHOST"