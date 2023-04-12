import pytest
from libgen_api.factory import (
    search_title,
    search_author,
    search_title_filtered,
    search_author_filtered,
)
from libgen_api.models import Request, Result, MIRROR_SOURCES

from . import title, title_request, author, author_request, short_search, Filters, fields_match


class TestBasicSearching:
    def test_title_search(self, title):
        titles = search_title(title)
        first = titles[0]

        assert title in first.title

    def test_author_search(self, author):
        titles = search_author(author)
        first = titles[0]

        assert author in first.author

    def test_resolve_download_links(self, author):
        titles = search_author(author)
        title_to_download = titles[0]
        dl_links = title_to_download.download_links

        # ensure each host is in the results and that they each have a url
        assert list(dl_links.keys()) == MIRROR_SOURCES
        assert all(dl_links.values())

    # should return an error if search query is less than 3 characters long
    def test_raise_error_on_short_search(self, short_search):
        with pytest.raises(Exception):
            titles = search_title(short_search)


class TestFilteredSearching:
    class TestExactFiltering:
        def test_title_filtering(self, title):
            title_filters = {"year": "2007", "extension": "epub"}
            titles = search_title_filtered(title, title_filters, exact_match=True)
            first_result = titles[0]

            assert title in first_result.title
            assert fields_match(title_filters, first_result)

        def test_author_filtering(self, author):
            filters = {"language": "German", "year": "2009"}
            titles = search_author_filtered(author, filters, exact_match=True)
            first_result = titles[0]

            assert author in first_result.author
            assert fields_match(filters, first_result)

        # explicit test of exact filtering
        # should return no results as they will all get filtered out
        def test_exact_filtering(self, author):
            exact_filters = {"xxtension": "PDF"}
            # if exact_match = True, this will filter out all results as
            # "pdf" is always written lower case on Library Genesis
            titles = search_author_filtered(author, exact_filters, exact_match=True)

            assert len(titles) == 0

    class TestInexactFiltering:
        def test_non_exact_filtering(self, author):
            filters = {"Extension": "PDF"}
            titles = search_author_filtered(author, filters, exact_match=False)
            first_result = titles[0]

            assert author in first_result.author
            assert fields_match(filters, first_result, exact=False)

    class TestPartialFiltering:
        def test_non_exact_partial_filtering(self, title):
            partial_filters = {"extension": "p", "Year": "200"}
            titles = search_title_filtered(title, partial_filters, exact_match=False)
            first_result = titles[0]

            assert title in first_result.title
            assert fields_match(partial_filters, first_result, exact=False)

        def test_exact_partial_filtering(self, title):
            exact_partial_filters = {"Extension": "p"}
            titles = search_title_filtered(title, exact_partial_filters, exact_match=True)

            assert len(titles) == 0
