from typing import Any

from fastapi import Depends, Query, APIRouter

from src2.application.list_category import CategorySortableFields, ListCategory, ListCategoryInput
from src2.application.listing import ListOutput
from src2.domain.category import Category
from src2.infra.api.http.dependencies import get_category_repository, common_parameters
from src2.infra.elasticsearch.elasticsearch_category_repository import ElasticsearchCategoryRepository

router = APIRouter()


@router.get("/", response_model=ListOutput[Category])
def list_categories(
    repository: ElasticsearchCategoryRepository = Depends(get_category_repository),
    sort: CategorySortableFields = Query(CategorySortableFields.NAME, description="Field to sort by"),
    common: dict[str, Any] = Depends(common_parameters),
) -> ListOutput[Category]:
    return ListCategory(repository=repository).execute(
        ListCategoryInput(
            search=common["search"],
            page=common["page"],
            per_page=common["per_page"],
            sort=sort,
            direction=common["direction"],
        )
    )
