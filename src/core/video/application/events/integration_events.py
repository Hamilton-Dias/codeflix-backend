from dataclasses import dataclass

from src.core._shared.events.event import Event


@dataclass(frozen=True)
class AudioVideoMediaUpdatedIntegrationEvent(Event):
  resource_id: str # <id>.<MediaType>
  file_path: str

  # def to_dict(self) -> dict:
  #   return {
  #     'resource_id': self.resource_id,
  #     'file_path': self.file_path
  #   }
