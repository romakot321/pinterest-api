import os
from loguru import logger
from aiohttp import ClientSession

from app.schemas.external import ExternalItem, ExternalRequest


class ExternalRepository:
    apify_token: str = os.getenv("APIFY_TOKEN", "")

    async def get_pinterest_pin_media(self, schema: ExternalRequest) -> list[ExternalItem]:
        async with ClientSession() as session:
            resp = await session.post(
                f"https://api.apify.com/v2/acts/easyapi~pinterest-image-downloader/run-sync-get-dataset-items?token={self.apify_token}",
                json=schema.model_dump()
            )
            assert resp.status == 201, await resp.text()
            data = await resp.json()
        logger.debug(f"Loaded {len(data)} pins")
        return [ExternalItem.model_validate(row) for row in data]

