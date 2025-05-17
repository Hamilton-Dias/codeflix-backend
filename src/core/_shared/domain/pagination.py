from abc import ABC
from dataclasses import dataclass

DEFAULT_PAGE_SIZE = 2

@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = DEFAULT_PAGE_SIZE
    total_items: int = 0


