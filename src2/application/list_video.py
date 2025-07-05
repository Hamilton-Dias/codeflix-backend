from enum import StrEnum

from src2.application.list_entity import ListEntity
from src2.application.listing import ListInput
from src2.domain.video import Video


class VideoSortableFields(StrEnum):
    TITLE = "title"


class ListVideoInput(ListInput):
    sort: VideoSortableFields | None = VideoSortableFields.TITLE


class ListVideo(ListEntity[Video]):
    pass
