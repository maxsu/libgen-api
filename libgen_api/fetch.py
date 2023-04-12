"""
Libgen URL parameters

Page 1 Reference URL
http://libgen.rs/search.php?req=test&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def
Request
req=test&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=defpage=3


Page 2 Reference URL
http://libgen.rs/search.php?&req=test&phrase=1&view=simple&column=def&sort=def&sortmode=ASC&page=3
Request
req=test&phrase=1&view=simple&column=def&sort=def&sortmode=ASC&page=3

Synthetic Request
http://libgen.rs/search.php?req=test&res=25&page=3
Request
req=test&res=25&page=3
"""

from urllib.parse import urlencode
from requests import get, Response

from .models import Page, Request

LIBGEN_URL = "http://gen.lib.rus.ec/search.php?"


def fetch(request: Request) -> Page:
    """
    Fetches a search page from liggen.

    Args:
        request : Request - The search request.

    Returns:
        Pages: The search page.
    """
    query_parsed = "+".join(request.query.split(" "))
    url_opts = {
        "req": query_parsed,
        "res": request.num_results,
        "page": request.page,
        "column": "title" if request.search_type == "title" else "author",
    }
    search_url = LIBGEN_URL + urlencode(url_opts)
    response: Response = get(search_url)
    page = Page(html=response.text)
    return page
