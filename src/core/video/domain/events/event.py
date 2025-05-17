
from dataclasses import dataclass
from uuid import UUID

from src.core.video.domain.value_objets import MediaType


@dataclass(frozen=True)
class AudioVideoMediaUpdated:
  aggregate_id: UUID
  file_path: str
  media_type: MediaType
