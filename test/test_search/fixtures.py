from operator import attrgetter
import pytest

from libgen_api.search import search, Request


@pytest.fixture
def title():
    return "Pride and Prejudice"


@pytest.fixture
def author():
    return "Agatha Christie"


@pytest.fixture
def long_request():
    return Request(
        query="test",
        search_type="title",
        num_results=300,
        results_per_page=100,
    )


@pytest.fixture
def long_result(long_request):
    return search(long_request)


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


@pytest.fixture
def results_length_invariant():
    ...
