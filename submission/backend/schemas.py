from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from .models import ShapeType, ColorType
from typing import Optional

class ShapeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    shape: ShapeType
    color: ColorType
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ShapeCreate(ShapeBase):
    pass

class ShapeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    shape: Optional[ShapeType] = None
    color: Optional[ColorType] = None

class ShapeResponse(ShapeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
