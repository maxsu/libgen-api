from operator import attrgetter
import pytest
from libgen_api.factory import (
    search_title,
    search_author,
    search_title_filtered,
    search_author_filtered,
)
from libgen_api.models import Request, Result, MIRROR_SOURCES


@pytest.fixture
def pride_and_prejudice():
    return "Pride and Prejudice"


@pytest.fixture
def agatha_christie():
    return "Agatha Christie"


@pytest.fixture
def pride_and_prejudice_request(pride_and_prejudice):
    return Request(
        query=pride_and_prejudice,
        search_type="title",
        num_results=3,
    )


@pytest.fixture
def agatha_christie_request(agatha_christie):
    return Request(
        query=agatha_christie,
        search_type="author",
        num_results=3,
    )


class TestBasicSearching:
    def test_title_search(self, pride_and_prejudice):
        titles = search_title(pride_and_prejudice)
        first = titles[0]

        assert pride_and_prejudice in first.title

    def test_author_search(self, agatha_christie):
        titles = search_author(agatha_christie)
        first = titles[0]

        assert agatha_christie in first.author

    def test_resolve_download_links(self, agatha_christie):
        titles = search_author(agatha_christie)
        title_to_download = titles[0]
        dl_links = title_to_download.download_links

        # ensure each host is in the results and that they each have a url
        assert list(dl_links.keys()) == MIRROR_SOURCES
        assert all(dl_links.values())

    # should return an error if search query is less than 3 characters long
    def test_raise_error_on_short_search(self):
        with pytest.raises(Exception):
            titles = search_title(pride_and_prejudice[0:2])


class TestFilteredSearching:
    class TestExactFiltering:
        def test_title_filtering(self, pride_and_prejudice):
            title_filters = {"year": "2007", "extension": "epub"}
            titles = search_title_filtered(pride_and_prejudice, title_filters, exact_match=True)
            first_result = titles[0]

            assert pride_and_prejudice in first_result.title
            assert fields_match(title_filters, first_result)

        def test_author_filtering(self, agatha_christie):
            filters = {"language": "German", "year": "2009"}
            titles = search_author_filtered(agatha_christie, filters, exact_match=True)
            first_result = titles[0]

            assert agatha_christie in first_result.author
            assert fields_match(filters, first_result)

        # explicit test of exact filtering
        # should return no results as they will all get filtered out
        def test_exact_filtering(self, agatha_christie):
            exact_filters = {"xxtension": "PDF"}
            # if exact_match = True, this will filter out all results as
            # "pdf" is always written lower case on Library Genesis
            titles = search_author_filtered(agatha_christie, exact_filters, exact_match=True)

            assert len(titles) == 0

    class TestInexactFiltering:
        def test_non_exact_filtering(self, agatha_christie):
            filters = {"Extension": "PDF"}
            titles = search_author_filtered(agatha_christie, filters, exact_match=False)
            first_result = titles[0]

            assert agatha_christie in first_result.author
            assert fields_match(filters, first_result, exact=False)

    class TestPartialFiltering:
        def test_non_exact_partial_filtering(self, pride_and_prejudice):
            partial_filters = {"extension": "p", "Year": "200"}
            titles = search_title_filtered(pride_and_prejudice, partial_filters, exact_match=False)
            first_result = titles[0]

            assert pride_and_prejudice in first_result.title
            assert fields_match(partial_filters, first_result, exact=False)

        def test_exact_partial_filtering(self, pride_and_prejudice):
            exact_partial_filters = {"Extension": "p"}
            titles = search_title_filtered(
                pride_and_prejudice, exact_partial_filters, exact_match=True
            )

            assert len(titles) == 0


####################
# Helper Functions #
####################


# Check object fields for equality -
# -> Returns True if they match.
# -> Returns False otherwise.
#
# when exact-True, fields are checked strictly (==).
#
# when exact=False, fields are normalized to lower case,
# and checked whether filter value is a subset of the response.
def fields_match(filter_obj, result: Result, exact=True):
    items = filter_obj.items()

    if exact:
        return all(attrgetter(key)(result) == value for key, value in items)
    else:
        return all(value.lower() in attrgetter(key.lower())(result).lower() for key, value in items)
