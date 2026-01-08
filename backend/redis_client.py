import json
import redis.asyncio as redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CHANNEL_NAME = "shapes_updates"

async def get_redis_client():
    return redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def publish_event(event_type: str, data: dict):
    client = await get_redis_client()
    message = {
        "type": event_type,
        "data": data
    }
    await client.publish(CHANNEL_NAME, json.dumps(message))
    await client.close()

async def event_generator():
    client = await get_redis_client()
    pubsub = client.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                yield message["data"]
    finally:
        await pubsub.unsubscribe(CHANNEL_NAME)
        await client.close()
