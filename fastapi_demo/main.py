import asyncio
import time

import httpx
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import Session

app = FastAPI()

engine_sync = create_engine(
    "postgresql://fastapi_demo:fastapi_demo@localhost/fastapi_demo"
)

engine_async = create_async_engine(
    "postgresql+asyncpg://fastapi_demo:fastapi_demo@localhost/fastapi_demo"
)

# Create Synchronous Session
sync_session = Session(engine_sync, expire_on_commit=False)
# Create Asynchronous Session
async_session = AsyncSession(engine_async, expire_on_commit=False)


@app.get("/sync")
def sync_get():
    start = time.time()
    sync_session.execute("SELECT pg_sleep(1)")
    with httpx.Client() as client:
        client.get("https://httpbin.org/delay/2")
        client.get("https://httpbin.org/delay/3")
    elapsed_seconds = time.time() - start
    return {"elapsed_time": f"{elapsed_seconds} seconds"}


@app.get("/async")
async def async_get():
    start = time.time()
    async with httpx.AsyncClient() as client:
        await asyncio.gather(
            async_session.execute("SELECT pg_sleep(1)"),
            client.get("https://httpbin.org/delay/2"),
            client.get("https://httpbin.org/delay/3"),
        )
    elapsed_seconds = time.time() - start
    return {"elapsed_time": f"{elapsed_seconds} seconds"}
