from uuid import UUID
from fastapi import Depends
from loguru import logger

from app.db.tables import Task, TaskItem
from app.repositories.external import ExternalRepository
from app.repositories.task import TaskRepository
from app.schemas.external import ExternalRequest
from app.schemas.task import TaskCreateSchema, TaskItemSchema, TaskSchema


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository = Depends(),
        external_repository: ExternalRepository = Depends(),
    ):
        self.task_repository = task_repository
        self.external_repository = external_repository

    async def create(self, schema: TaskCreateSchema) -> TaskSchema:
        model = Task(app_bundle=schema.app_bundle, user_id=schema.user_id)
        model = await self.task_repository.create(model)
        return TaskSchema.model_validate(model)

    async def send(self, schema: TaskCreateSchema, task_id: UUID):
        request = ExternalRequest(links=schema.urls)
        try:
            response = await self.external_repository.get_pinterest_pin_media(request)
        except AssertionError as e:
            logger.exception(e)
            await self.task_repository.update(task_id, error=str(e))
            return

        items = [
            TaskItem(
                author=item.result.author,
                title=item.result.title,
                error=(item.result.message if item.result.error else None),
                width=item.result.medias[-1].width if item.result.medias else None,
                height=item.result.medias[-1].height if item.result.medias else None,
                url=item.result.medias[-1].url if item.result.medias else None,
                thumbnail=item.result.medias[-1].thumbnail if item.result.medias else None,
                type=item.result.medias[-1].type if item.result.medias else None,
                task_id=task_id,
            )
            for item in response
        ]
        await self.task_repository.create_items(*items)

    async def get(self, task_id: UUID) -> TaskSchema:
        model = await self.task_repository.get(task_id)
        return TaskSchema.model_validate(model)
