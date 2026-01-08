from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import json
import asyncio
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from . import crud, schemas, database, redis_client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

get_db = database.get_db

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/shapes", response_model=List[schemas.ShapeResponse])
async def read_shapes(db: AsyncSession = Depends(get_db)):
    return await crud.get_shapes(db)

@app.post("/api/shapes", response_model=schemas.ShapeResponse)
async def create_shape(shape: schemas.ShapeCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_shape(db, shape)

@app.put("/api/shapes/{id}", response_model=schemas.ShapeResponse)
async def update_shape(id: int, shape: schemas.ShapeUpdate, db: AsyncSession = Depends(get_db)):
    updated_shape = await crud.update_shape(db, id, shape)
    if not updated_shape:
        raise HTTPException(status_code=404, detail="Shape not found")
    return updated_shape

@app.delete("/api/shapes/{id}")
async def delete_shape(id: int, db: AsyncSession = Depends(get_db)):
    deleted_shape = await crud.delete_shape(db, id)
    if not deleted_shape:
        raise HTTPException(status_code=404, detail="Shape not found")
    return {"status": "success", "id": id}

@app.get("/api/events/stream")
async def sse_stream(request: Request):
    async def sse_generator():
        client = await redis_client.get_redis_client()
        pubsub = client.pubsub()
        await pubsub.subscribe(redis_client.CHANNEL_NAME)
        
        try:
            while True:
                if await request.is_disconnected():
                    break

                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                
                if message:
                     raw_data = message['data']
                     yield f"event: shapes\ndata: {raw_data}\n\n"
                
                yield f"event: ping\ndata: {json.dumps({'ts': datetime.utcnow().isoformat()})}\n\n"

        except asyncio.CancelledError:
            pass
        finally:
            await pubsub.unsubscribe(redis_client.CHANNEL_NAME)
            await client.close()

    return StreamingResponse(sse_generator(), media_type="text/event-stream")
