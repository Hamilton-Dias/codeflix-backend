from dataclasses import dataclass
from enum import StrEnum
from src.core._shared.domain.entity import Entity

class CastMemberType(StrEnum):
  ACTOR = "ACTOR"
  DIRECTOR = "DIRECTOR"

@dataclass
class CastMember(Entity):
  name: str = ""
  type: CastMemberType = CastMemberType.ACTOR

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
  
  def update_cast_member(self, name, type):
    self.name = name
    self.type = type

    self.validate()
