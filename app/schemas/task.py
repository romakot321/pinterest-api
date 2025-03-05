from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class TaskCreateSchema(BaseModel):
    user_id: str
    app_bundle: str
    urls: list[str]


class TaskItemType(Enum):
    video = "video"
    image = "image"


class TaskItemSchema(BaseModel):
    author: str | None = None
    title: str | None = None
    error: str | None = None

    width: int | None = None
    height: int | None = None
    url: str | None = None
    thumbnail: str | None = None  # For video only
    type: TaskItemType | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskSchema(BaseModel):
    id: UUID
    error: str | None = None
    items: list[TaskItemSchema]

    model_config = ConfigDict(from_attributes=True)

