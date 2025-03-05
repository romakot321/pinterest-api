from pydantic import BaseModel


class ExternalItem(BaseModel):
    class Result(BaseModel):
        class ResultMedia(BaseModel):
            width: int
            height: int
            url: str
            thumbnail: str | None = None  # When video
            type: str

        author: str | None = None
        title: str | None = None
        medias: list[ResultMedia] | None = None
        error: bool = False
        message: str | None = None  # When error

    url: str
    result: Result


class ExternalRequest(BaseModel):
    links: list[str]
