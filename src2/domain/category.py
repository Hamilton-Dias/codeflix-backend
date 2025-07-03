from src2.domain.entity import Entity


class Category(Entity):
    name: str
    description: str = ""
