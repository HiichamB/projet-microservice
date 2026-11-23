"""Publication d'événements (TP6)."""
import json
import os
import uuid

import aio_pika

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")


async def publier(routing_key: str, payload: dict) -> None:
    connexion = await aio_pika.connect(  # PAS connect_robust :
        RABBITMQ_URL,
        timeout=2,  # échouer vite si le broker est coupé (leçon TP5)
    )
    async with connexion:
        canal = await connexion.channel()
        exchange = await canal.declare_exchange("events", aio_pika.ExchangeType.TOPIC)
        message = aio_pika.Message(
            body=json.dumps({"message_id": str(uuid.uuid4()), **payload}).encode(),
            content_type="application/json",
        )
        await exchange.publish(message, routing_key=routing_key)
