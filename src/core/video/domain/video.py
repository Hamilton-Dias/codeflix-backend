from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from src.core._shared.domain.entity import Entity
from src.core.video.domain.events.event import AudioVideoMediaUpdated
from src.core.video.domain.value_objets import AudioVideoMedia, ImageMedia, MediaStatus, MediaType, Rating


@dataclass(eq=False)
class Video(Entity):
  title: str
  description: str
  launch_year: int
  duration: Decimal
  rating: Rating
  opened: bool
  published: bool = field(default=False, init=False)

  categories: set[UUID]
  genres: set[UUID]
  cast_members: set[UUID]

  banner: ImageMedia | None = None
  thumbnail: ImageMedia | None = None
  thumbnail_half: ImageMedia | None = None
  trailer: AudioVideoMedia | None = None
  video: AudioVideoMedia | None = None

  def __post_init__(self):
    self.validate()

  def validate(self):
    if len(self.title) > 255:
      self.notification.add_error("Title must be less than 255 characters")
      
    if not self.title:
      self.notification.add_error("Title is required")

    if self.notification.has_errors:
      raise ValueError(self.notification.messages)
    
  def publish(self) -> None:
    if not self.video:
      self.notification.add_error("Video must have media to be published")
    elif self.video.status != MediaStatus.COMPLETED:
      self.notification.add_error("Video must be completed to be published")

    self.published = True
    self.validate()

  def update(self, title, description, launch_year, duration, published, rating, opened):
    self.title = title
    self.description = description
    self.launch_year = launch_year
    self.duration = duration
    self.published = published
    self.rating = rating
    self.opened = opened

    self.validate()

  def add_category(self, category_id: UUID) -> None:
    self.categories.add(category_id)
    self.validate()
  
  def add_genre(self, genre_id: UUID) -> None:
    self.genres.add(genre_id)
    self.validate()

  def add_cast_member(self, cast_member_id: UUID) -> None:
    self.cast_members.add(cast_member_id)
    self.validate()

  def update_banner(self, banner: ImageMedia) -> None:
    self.banner = banner
    self.validate()

  def update_thumbnail(self, thumbnail: ImageMedia) -> None:
    self.thumbnail = thumbnail
    self.validate()

  def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
    self.thumbnail_half = thumbnail_half
    self.validate()

  def update_trailer(self, trailer: AudioVideoMedia) -> None:
    self.trailer = trailer
    self.validate()

  def update_video(self, video: AudioVideoMedia) -> None:
    self.video = video
    self.validate()
    self.dispatch(AudioVideoMediaUpdated(
      aggregate_id=self.id,
      file_path=video.raw_location,
      media_type=MediaType.VIDEO
    ))

  def process(self, status: MediaStatus, encoded_location: str) -> None:
    if status == MediaStatus.COMPLETED:
      self.video = AudioVideoMedia(
        name=self.video.name,
        raw_location=self.video.raw_location,
        encoded_location=encoded_location,
        status=MediaStatus.COMPLETED,
        media_type=MediaType.VIDEO
      )
      self.publish()
    else:
      self.video = AudioVideoMedia(
        name=self.video.name,
        raw_location=self.video.raw_location,
        encoded_location="",
        status=MediaStatus.ERROR,
        media_type=MediaType.VIDEO
      )

    self.validate()
