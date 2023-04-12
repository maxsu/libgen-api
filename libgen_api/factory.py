from .models import Request, Results
from .search import search


def search_title(query: str) -> Results:
    request = Request(query, search_type="title")
    return search(request)


def search_author(query: str) -> Results:
    request = Request(query, search_type="author")
    return search(request)


def search_title_filtered(
    query: str,
    filters,
    exact_match=True,
) -> Results:
    request = Request(query, search_type="title")
    results = search(request)
    filtered_results = results.filter(filters, exact_match)
    return filtered_results


def search_author_filtered(
    query: str,
    filters,
    exact_match=True,
) -> Results:
    search_request = Request(query, search_type="author")
    results = search(search_request)
    filtered_results = results.filter(filters, exact_match)
    return filtered_results
