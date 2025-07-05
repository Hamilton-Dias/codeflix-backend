from abc import ABC, abstractmethod

from src2.domain.repository import Repository
from src2.domain.video import Video


class VideoRepository(Repository[Video], ABC):
    @abstractmethod
    def save(self, video: Video) -> None:
        raise NotImplementedError
