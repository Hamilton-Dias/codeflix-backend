from dataclasses import dataclass
from uuid import UUID
from dataclasses import field
import uuid
from enum import StrEnum, auto

class CastMemberType(StrEnum):
  ACTOR = auto()
  DIRECTOR = auto()

@dataclass
class CastMember:
  id: UUID = field(default_factory=uuid.uuid4)
  name: str = ""
  type: CastMemberType = CastMemberType.ACTOR

  def __post_init__(self):
    self.validate()

  def validate(self):
    if not self.name:
      raise ValueError("Name must be provided")
    
    if self.name == '':
      raise ValueError("Name must not be empty")
    
    if not self.type:
      raise ValueError("Type must be provided")
    
    if self.type not in CastMemberType:
      raise ValueError("Type must be valid")
    
  def __repr__(self):
    return f"<CastMember {self.name} ({self.id})>"
  
  def __eq__(self, other):
    return isinstance(other, CastMember) and self.id == other.id
  
  
