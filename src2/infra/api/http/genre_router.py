from typing import Any

from fastapi import Depends, Query, APIRouter

from src2.application.list_genre import GenreSortableFields, ListGenre, ListGenreInput
from src2.application.listing import ListOutput
from src2.domain.genre import Genre
from src2.domain.genre_repository import GenreRepository
from src2.infra.api.http.dependencies import common_parameters, get_genre_repository

router = APIRouter()


@router.get("/", response_model=ListOutput[Genre])
def list_genres(
    repository: GenreRepository = Depends(get_genre_repository),
    sort: GenreSortableFields = Query(GenreSortableFields.NAME, description="Field to sort by"),
    common: dict[str, Any] = Depends(common_parameters),
) -> ListOutput[Genre]:
    return ListGenre(repository=repository).execute(
        ListGenreInput(
            search=common["search"],
            page=common["page"],
            per_page=common["per_page"],
            sort=sort,
            direction=common["direction"],
        )
    )
