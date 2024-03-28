from os import environ
import redis.asyncio as redis


async def get_redis():
    return await redis.from_url(
        environ['VT_REDIS_URL'],
        encoding="utf-8",
        decode_responses=True,
        #ssl_cert_reqs=None  # self-sign certification도 받아들여
    )
