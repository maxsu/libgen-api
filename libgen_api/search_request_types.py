from abc import ABC
import requests
from bs4 import BeautifulSoup


class ISearchRequest(ABC):
    col_names: list[str]

    def __init__(self, query: str, search_type: str = "title") -> None:
        """
        :param query: the search query to be used
        :type query: str
        :param search_type: the type of search to be performed. Defaults to 'title'.
        :type search_type: str
        """
        ...

    def strip_i_tag_from_soup(self, soup: BeautifulSoup) -> None:
        """
        Strips the <i> tag from the soup object.

        :param soup: the BeautifulSoup object to be processed
        :type soup: BeautifulSoup
        """
        ...

    def get_search_page(self) -> requests.Response:
        """
        Fetches the search page from gen.lib.rus.ec.

        :return: the search page
        :rtype: requests.Response
        """
        ...

    def aggregate_request_data(self) -> list[dict[str, str]]:
        """
        Aggregates the request data from the search page.

        :return: a list of dictionaries representing the data
        :rtype: list[dict[str, str]]
        """
        ...
