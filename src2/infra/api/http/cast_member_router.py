from typing import Any

from fastapi import Depends, Query, APIRouter

from src2.application.list_cast_member import CastMemberSortableFields, ListCastMember, ListCastMemberInput
from src2.application.listing import ListOutput
from src2.domain.cast_member import CastMember
from src2.infra.api.http.dependencies import common_parameters, get_cast_member_repository
from src2.infra.elasticsearch.elasticsearch_cast_member_repository import ElasticsearchCastMemberRepository

router = APIRouter()


@router.get("/", response_model=ListOutput[CastMember])
def list_cast_members(
    repository: ElasticsearchCastMemberRepository = Depends(get_cast_member_repository),
    sort: CastMemberSortableFields = Query(CastMemberSortableFields.NAME, description="Field to sort by"),
    common: dict[str, Any] = Depends(common_parameters),
) -> ListOutput[CastMember]:
    return ListCastMember(repository=repository).execute(
        ListCastMemberInput(
            search=common["search"],
            page=common["page"],
            per_page=common["per_page"],
            sort=sort,
            direction=common["direction"],
        )
    )
