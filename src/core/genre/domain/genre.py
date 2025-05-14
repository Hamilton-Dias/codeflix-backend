from dataclasses import dataclass
from uuid import UUID
from dataclasses import field
import uuid

from src.core.category.domain.notification import Notification

@dataclass
class Genre:
  name: str
  is_active: bool = True
  id: UUID = field(default_factory=uuid.uuid4)
  categories: set[UUID] = field(default_factory=set)

  notification: Notification = field(default_factory=Notification)

  def __post_init__(self):
    self.validate()
    
  def validate(self):
    if len(self.name) > 255:
      self.notification.add_error("Name must be less than 256 characters")
    
    if not self.name:
      self.notification.add_error("Name must be provided")
    
    if self.notification.has_errors:
      raise ValueError(self.notification.messages)

  def __str__(self):
    return f"{self.name} - ({self.is_active})"
  
  def __repr__(self):
    return f"<Genre {self.name} ({self.id})>"
  
  def __eq__(self, other):
    return isinstance(other, Genre) and self.id == other.id
  
  def update_genre(self, name):
    self.name = name

    self.validate()

  def activate(self):
    self.is_active = True

    self.validate()
  
  def deactivate(self):
    self.is_active = False

    self.validate()

  def add_category(self, category_id: UUID):
    self.categories.add(category_id)
    self.validate()

  def remove_category(self, category_id: UUID):
    self.categories.remove(category_id)
    self.validate()
