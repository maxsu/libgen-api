from dataclasses import dataclass


@dataclass
class Request:
    query: str
    search_type: str = "title"
    num_results: int = 25
    page: int = 1
