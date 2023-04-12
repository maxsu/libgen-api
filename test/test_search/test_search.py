import pytest

from libgen_api.models import Request, Result, Results, MIRROR_SOURCES
from libgen_api.search import search

from . import (
    author,
    author_request,
    author_results,
    title,
    title_request,
    title_results,
    short_search,
    Filters,
    fields_match,
)


class TestBasicSearching:
    def test_title_search(self, title: str, title_results: Request):
        first = title_results[0]
        assert title in first.title

    def test_author_search(self, author: str, author_results: Results):
        assert all(author in item.author for item in author_results)

    def test_resolve_download_links(self, author_results: Results):
        title_to_download = author_results[0]
        download_links = title_to_download.download_links

        # download_links values are nonempty urls
        assert all(download_links.values())

        # download_links has keys from MIRROR_SOURCES
        assert list(download_links.keys()) == MIRROR_SOURCES

    def test_raise_error_on_short_search(self, short_search: Request):
        # should return an error if search query is less than 3 characters long
        with pytest.raises(Exception):
            search(short_search)


class TestResultFiltering:
    class TestExactFiltering:
        def test_title_filtering(self, title, title_results):
            titles = title_results.filter(Filters.year_extension, exact_match=True)
            first_result = titles[0]

            assert title in first_result.title
            assert fields_match(Filters.year_extension, first_result)

        def test_author_filtering(self, author, author_results):
            filters = {"language": "German", "year": "2009"}

            titles = author_results.filter(filters, exact_match=True)
            first_result = titles[0]

            assert author in first_result.author
            assert fields_match(filters, first_result)

        # explicit test of exact filtering
        # should return no results as they will all get filtered out
        def test_exact_filtering(self, author_results):
            # this will filter out all results. "pdf" is lower case on Library Genesis
            titles = author_results.filter(Filters.inexact, exact_match=True)
            titles2 = author_results.filter(Filters.inexact2, exact_match=True)
            assert len(titles) == 0
            assert len(titles2) == 0

    class TestInexactFiltering:
        def test_inexact_filtering(self, author, author_results):
            titles = author_results.filter(Filters.inexact2, exact_match=False)
            first_result = titles[0]

            assert author in first_result.author
            assert fields_match(Filters.inexact2, first_result, exact=False)

    class TestPartialFiltering:
        def test_inexact_partial_filtering(self, title, title_results):
            titles = title_results.filter(Filters.partial_inexact, exact_match=False)
            first_result = titles[0]

            assert title in first_result.title
            assert fields_match(Filters.partial_inexact, first_result, exact=False)

        def test_exact_partial_filtering(self, title_results):
            titles = title_results.filter(Filters.partial_exact, exact_match=True)

            assert len(titles) == 0
