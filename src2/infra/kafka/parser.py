import json
import logging
from dataclasses import dataclass
from typing import Type

from src2.domain.cast_member import CastMember
from src2.domain.category import Category
from src2.domain.entity import Entity
from src2.domain.genre import Genre
from src2.domain.video import Video
from src2.infra.kafka.operation import Operation

logger = logging.getLogger(__name__)


@dataclass
class ParsedEvent:
    entity: Type[Entity]
    operation: Operation
    payload: dict


table_to_entity = {
    "categories": Category,
    "cast_members": CastMember,
    "genres": Genre,
    "videos": Video,
}


def parse_debezium_message(data: bytes) -> ParsedEvent | None:
    try:
        json_data = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError as e:
        logger.error(e)
        return None

    try:
        entity = table_to_entity[json_data["payload"]["source"]["table"]]
        operation = Operation(json_data["payload"]["op"])
        payload = json_data["payload"]["after"] if operation != Operation.DELETE else json_data["payload"]["before"]
    except (KeyError, ValueError) as e:
        logger.error(e)
        return None

    return ParsedEvent(entity=entity, operation=operation, payload=payload)
