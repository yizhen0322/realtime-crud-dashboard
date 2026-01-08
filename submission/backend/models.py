from datetime import datetime
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
import enum

class ShapeType(str, enum.Enum):
    circle = "circle"
    triangle = "triangle"
    square = "square"

class ColorType(str, enum.Enum):
    red = "red"
    green = "green"
    blue = "blue"
    yellow = "yellow"
    black = "black"

class Shape(Base):
    __tablename__ = "shapes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    shape: Mapped[ShapeType] = mapped_column(Enum(ShapeType), nullable=False)
    color: Mapped[ColorType] = mapped_column(Enum(ColorType), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
