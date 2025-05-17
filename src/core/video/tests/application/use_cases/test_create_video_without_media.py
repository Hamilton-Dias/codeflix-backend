import pytest
import uuid
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMediaUseCase
from src.core.video.domain.video import Video, Rating
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.video.application.exceptions import RelatedEntitiesNotFound, InvalidVideo

class TestCreateVideoWithoutMedia:
  def test_execute_with_valid_input(self):
    video_repo = InMemoryVideoRepository()
    category_repo = InMemoryCategoryRepository()
    genre_repo = InMemoryGenreRepository()
    cast_member_repo = InMemoryCastMemberRepository()

    use_case = CreateVideoWithoutMediaUseCase(
      video_repository=video_repo,
      category_repository=category_repo,
      cast_members_repository=cast_member_repo,
      genres_repository=genre_repo
    )
    
    category = Category(name="Movie")
    genre = Genre(name="Action")
    cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)

    category_repo.save(category)
    genre_repo.save(genre)
    cast_member_repo.save(cast_member)
    
    input_data = CreateVideoWithoutMediaUseCase.Input(
      title="Test Video",
      description="Test Description",
      launch_year=2023,
      duration=120,
      rating=Rating.L,
      published=False,
      categories={category.id},
      genres={genre.id},
      cast_members={cast_member.id}
    )
    
    output = use_case.execute(input_data)
    
    assert isinstance(output.id, uuid.UUID)
    assert len(video_repo.videos) == 1
    saved_video = video_repo.videos[0]
    assert saved_video.title == "Test Video"
    assert saved_video.published is False

  def test_execute_with_invalid_title(self):
    video_repo = InMemoryVideoRepository()
    category_repo = InMemoryCategoryRepository()
    genre_repo = InMemoryGenreRepository()
    cast_member_repo = InMemoryCastMemberRepository()

    use_case = CreateVideoWithoutMediaUseCase(
      video_repository=video_repo,
      category_repository=category_repo,
      cast_members_repository=cast_member_repo,
      genres_repository=genre_repo
    )
    
    input_data = CreateVideoWithoutMediaUseCase.Input(
      title="",
      description="Test Description",
      launch_year=2023,
      duration=120,
      published=False,
      rating=Rating.L,
      categories=set(),
      genres=set(),
      cast_members=set()
    )
    
    with pytest.raises(InvalidVideo):
      use_case.execute(input_data)

  def test_execute_with_invalid_related_entities(self):
    video_repo = InMemoryVideoRepository()
    use_case = CreateVideoWithoutMediaUseCase(video_repo)
    
    fake_id = uuid.uuid4()
    input_data = CreateVideoWithoutMediaUseCase.Input(
      title="Test Video",
      description="Test Description",
      launch_year=2023,
      duration=120,
      rating=Rating.L,
      categories=[fake_id],
      genres=[fake_id],
      cast_members=[fake_id]
    )
    
    with pytest.raises(RelatedEntitiesNotFound):
      use_case.execute(input_data)
