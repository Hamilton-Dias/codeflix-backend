
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.notification import Notification
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import RelatedEntitiesNotFound, InvalidVideo
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class CreateVideoWithoutMediaUseCase:
  
  @dataclass
  class Input:
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: str
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]

  @dataclass
  class Output:
    id: UUID

  def __init__(
      self, 
      video_repository: VideoRepository,
      category_repository: CategoryRepository,
      cast_members_repository: CastMemberRepository,
      genres_repository: GenreRepository
    ) -> None:
      self.video_repository = video_repository
      self.category_repository = category_repository
      self.cast_members_repository = cast_members_repository
      self.genres_repository = genres_repository

  def execute(self, input: Input) -> Output:
    notification = Notification()

    self.validate_categories(input, notification)
    self.validate_cast_members(input, notification)
    self.validate_genres(input, notification)

    if notification.has_errors:
      raise RelatedEntitiesNotFound(notification.messages)

    try:
      video = Video(
        title=input.title,
        description=input.description,
        launch_year=input.launch_year,
        duration=input.duration,
        published=False,
        rating=input.rating,
        categories=input.categories,
        genres=input.genres,
        cast_members=input.cast_members
      )
    except ValueError as exception:
      raise InvalidVideo(exception)

    self.video_repository.save(video)

    return self.Output(id=video.id)
  
  def validate_categories(self, input: Input, notification: Notification) -> None:
    categories = {category.id for category in self.category_repository.list()}
    if not input.categories.issubset(categories):
      notification.add_error(f"Categories not found: {input.categories - categories}")

  def validate_cast_members(self, input: Input, notification: Notification) -> None:
    cast_members = {cast_member.id for cast_member in self.cast_members_repository.list()}
    if not input.cast_members.issubset(cast_members):
      notification.add_error(f"CastMembers not found: {input.cast_members - cast_members}")

  def validate_genres(self, input: Input, notification: Notification) -> None:
    genres = {genre.id for genre in self.genres_repository.list()}
    if not input.genres.issubset(genres):
      notification.add_error(f"Genres not found: {input.genres - genres}")
