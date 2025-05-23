from dataclasses import dataclass
from enum import Enum, StrEnum, auto, unique
from uuid import UUID

@unique
class MediaStatus(StrEnum):
  PENDING = "PENDING"
  PROCESSING = "PROCESSING"
  COMPLETED = "COMPLETED"
  ERROR = "ERROR"

@unique
class MediaType(StrEnum):
    VIDEO = "VIDEO"
    TRAILER = "TRAILER"
    BANNER = "BANNER"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_HALF = "THUMBNAIL_HALF"

@unique
class Rating(Enum):
  ER = auto()
  L = auto()
  AGE_10 = auto()
  AGE_12 = auto()
  AGE_14 = auto()
  AGE_16 = auto()
  AGE_18 = auto()

@dataclass(frozen=True)
class ImageMedia:
  name: str
  location: str

@dataclass(frozen=True)
class AudioVideoMedia:
  name: str
  raw_location: str
  encoded_location: str
  status: MediaStatus
  media_type: MediaType
