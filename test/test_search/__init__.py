from operator import attrgetter
import pytest

from libgen_api.models import Request, Result, MIRROR_SOURCES
from libgen_api.search import search


@pytest.fixture
def title():
    return "Pride and Prejudice"


@pytest.fixture
def author():
    return "Agatha Christie"


@pytest.fixture
def title_request(title):
    return Request(
        query=title,
        search_type="title",
    )


@pytest.fixture
def author_request(author):
    return Request(
        query=author,
        search_type="author",
    )


@pytest.fixture
def short_search():
    return Request(
        query="aaa",
    )


# Cache the result of the search for the test cases
@pytest.fixture
def author_results(author_request: Request):
    return search(author_request)


@pytest.fixture
def title_results(title_request: Request):
    return search(title_request)


class Filters:
    year_extension = {"year": "2007", "extension": "epub"}
    inexact = {"extension": "PDF"}
    inexact2 = {"ExTeNsIon": "PDF"}
    exact = {"extension": "pdf"}
    partial_exact = {"extension": "p", "year": "200"}
    partial_inexact = {"extension": "p", "Year": "200"}


####################
# Helper Functions #
####################


"""
Check object fields for equality -

Args:
filter_obj: object to check
-> Returns True if they match.
-> Returns False otherwise.

when exact-True, fields are checked strictly (==).

when exact=False, we normalize fields and filter values to lower case,
then check if filter value is a subset of the result.
"""


def fields_match(filter: dict[str, str], result: Result, exact=True):
    items = filter.items()

    if exact:
        return all(attrgetter(key)(result) == value for key, value in items)

    return all(value.lower() in attrgetter(key.lower())(result).lower() for key, value in items)
