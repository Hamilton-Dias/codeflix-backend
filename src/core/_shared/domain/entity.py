from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID
import uuid

from src.core._shared.domain.notification import Notification
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.event import Event
from src.core._shared.events.message_bus import MessageBus

@dataclass(kw_only=True, eq=False)
class Entity(ABC):
  id: UUID = field(default_factory=uuid.uuid4)
  notification: Notification = field(default_factory=Notification, init=False)
  events: list[Event] = field(default_factory=list, init=False)
  message_bus: AbstractMessageBus = field(default_factory=MessageBus)

  def dispatch(self, event: Event) -> None:
    self.events.append(event)
    self.message_bus.handle(self.events)

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.id == other.id

  @abstractmethod
  def validate(self):
    pass
