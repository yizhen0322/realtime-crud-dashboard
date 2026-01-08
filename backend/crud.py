from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models, schemas, redis_client

async def get_shapes(db: AsyncSession):
    result = await db.execute(select(models.Shape))
    return result.scalars().all()

async def get_shape(db: AsyncSession, shape_id: int):
    result = await db.execute(select(models.Shape).where(models.Shape.id == shape_id))
    return result.scalar_one_or_none()

async def create_shape(db: AsyncSession, shape: schemas.ShapeCreate):
    db_shape = models.Shape(**shape.model_dump())
    db.add(db_shape)
    await db.commit()
    await db.refresh(db_shape)
    
    await redis_client.publish_event("created", {
        "id": db_shape.id,
        "name": db_shape.name,
        "shape": db_shape.shape,
        "color": db_shape.color,
        "timestamp": db_shape.timestamp.isoformat()
    })
    return db_shape

async def update_shape(db: AsyncSession, shape_id: int, shape_update: schemas.ShapeUpdate):
    db_shape = await get_shape(db, shape_id)
    if not db_shape:
        return None
    
    update_data = shape_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_shape, key, value)
    
    await db.commit()
    await db.refresh(db_shape)

    await redis_client.publish_event("updated", {
        "id": db_shape.id,
        "name": db_shape.name,
        "shape": db_shape.shape,
        "color": db_shape.color,
        "timestamp": db_shape.timestamp.isoformat()
    })
    return db_shape

async def delete_shape(db: AsyncSession, shape_id: int):
    db_shape = await get_shape(db, shape_id)
    if not db_shape:
        return None
    
    await db.delete(db_shape)
    await db.commit()

    await redis_client.publish_event("deleted", {"id": shape_id})
    return db_shape
