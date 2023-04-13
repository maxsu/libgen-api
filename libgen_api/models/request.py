from dataclasses import dataclass


@dataclass
class Request:
    query: str
    search_type: str = "title"
    fetch_page: int = 1
    results_per_page: int = 25
    num_results: int = 25
