from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID
import uuid

from src.core._shared.domain.notification import Notification


@dataclass(kw_only=True)
class Entity(ABC):
  id: UUID = field(default_factory=uuid.uuid4)
  notification: Notification = field(default_factory=Notification)

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.id == other.id

  @abstractmethod
  def validate(self):
    pass
