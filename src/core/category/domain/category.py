from dataclasses import dataclass
from uuid import UUID
from dataclasses import field
import uuid

@dataclass
class Category:
  name: str
  id: UUID = field(default_factory=uuid.uuid4)
  description: str = ""
  is_active: bool = True

  def __post_init__(self):
    self.validate()
    
  def validate(self):
    if len(self.name) > 255:
      raise ValueError("Name must be less than 256 characters")
    
    if not self.name:
      raise ValueError("Name must be provided")

  def __str__(self):
    return f"{self.name} - {self.description} ({self.is_active})"
  
  def __repr__(self):
    return f"<Category {self.name} ({self.id})>"
  
  def __eq__(self, other):
    return isinstance(other, Category) and self.id == other.id
  
  def update_category(self, name, description):
    self.name = name
    self.description = description

    self.validate()

  def activate(self):
    self.is_active = True

    self.validate()
  
  def deactivate(self):
    self.is_active = False

    self.validate()
