from typing import Type
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.event import Event
from src.core._shared.application.handler import Handler


class MessageBus(AbstractMessageBus):  
  def __init__(self) -> None:
    self.handlers: dict[Type[Event], list[Handler]] = {}

  def handle(self, events: list[Event]) -> None:
    for event in events:
      handlers = self.handlers[type(event)]
      for handler in handlers:
        handler.handle(event)
