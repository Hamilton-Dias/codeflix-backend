from django.db import models
from uuid import uuid4

from src.core.cast_member.domain.cast_member import CastMemberType

class CastMember(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid4)
  name = models.CharField(max_length=255)
  type = models.CharField(choices=[(tag.name, tag.value) for tag in CastMemberType])

  class Meta:
    db_table = "cast_member"

  def __str__(self):
    return self.name
