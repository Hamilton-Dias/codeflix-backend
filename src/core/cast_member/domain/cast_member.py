from dataclasses import dataclass
from uuid import UUID
from dataclasses import field
import uuid
from enum import StrEnum

from src.core.category.domain.notification import Notification

class CastMemberType(StrEnum):
  ACTOR = "ACTOR"
  DIRECTOR = "DIRECTOR"

@dataclass
class CastMember:
  id: UUID = field(default_factory=uuid.uuid4)
  name: str = ""
  type: CastMemberType = CastMemberType.ACTOR

  notification: Notification = field(default_factory=Notification)

  def __post_init__(self):
    self.validate()

  def validate(self):
    if not self.name:
      self.notification.add_error("Name must be provided")
    
    if self.name == '':
      self.notification.add_error("Name must not be empty")
    
    if not self.type:
      self.notification.add_error("Type must be provided")
    
    if self.type not in CastMemberType:
      self.notification.add_error("Type must be valid")
    
    if self.notification.has_errors:
      raise ValueError(self.notification.messages)
    
  def __repr__(self):
    return f"<CastMember {self.name} ({self.id})>"
  
  def __eq__(self, other):
    return isinstance(other, CastMember) and self.id == other.id
  
  def update_cast_member(self, name, type):
    self.name = name
    self.type = type

    self.validate()
