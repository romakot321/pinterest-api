from fastapi import APIRouter, BackgroundTasks, Depends
from uuid import UUID

from app.schemas.task import TaskCreateSchema, TaskSchema
from app.services.task import TaskService
from . import validate_api_token


router = APIRouter(prefix="/api/task", tags=["Task"])


@router.post("", response_model=TaskSchema)
async def create_task(
        schema: TaskCreateSchema,
        background_tasks: BackgroundTasks,
        service: TaskService = Depends()
):
    model = await service.create(schema)
    background_tasks.add_task(service.send, schema, model.id)
    return model


@router.get("/{task_id}")
async def get_task(
        task_id: UUID,
        service: TaskService = Depends()
):
    return await service.get(task_id)

