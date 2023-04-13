"""
The SearchRequest module lets us build and process search libgen search queries.

Usage:
    from libgen_api import search, Request
    request = Request(query="...", search_type="title", num_results=25)
    results = search(request)
"""

from .models import Request, Results
from .fetch import fetch
from .scrape import scrape


def search(request: Request) -> Results:
    """
    Fulfills a libgen search request.

    Returns a list of results that match the given search criteria:

        num_results: The number of results to return.
            >0 returns the first num_results results.
            -1 returns all results.

        query: The search query.

        search_type: The type of search to perform.

    Args:
        request : Request - The search request.

    Returns:
        Results: The search results.
    """

    results = Results()

    def need_more_results():
        return request.num_results == -1 or request.num_results > len(results)

    while need_more_results():
        search_page = fetch(request)
        page_results = scrape(search_page)
        results += page_results

        results_mismatch = len(page_results) != page_results.page_max - page_results.page_min + 1
        results_meet_request_max = len(results) >= request.num_results and request.num_results != -1
        results_meet_page_max = len(results) == page_results.max_num
        results_exceed_page_max = len(results) > page_results.max_num
        # todo: Warn the user if we exceeded / mismatch

        if results_exceed_page_max:
            raise Exception("Results exceeded page max")

        if results_mismatch:
            raise Exception("Results mismatch")

        if not results or results_meet_page_max or results_meet_request_max:
            break

        request.fetch_page += 1

    return results
