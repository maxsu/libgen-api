import re
from bs4 import BeautifulSoup, PageElement, ResultSet

from .models import Page, Results, Result


def scrape(page: Page) -> Results:
    """
    Extracts the result data from the search page.

    Args:
        page : Page - The search page.

    Returns:
        Results: The search results.
    """

    soup = BeautifulSoup(page.html, "lxml")
    strip_i_tags(soup)

    page_min, page_max, max_count = get_max_count(soup)

    results_table: ResultSet = soup.find_all("table")[2]
    rows = results_table.find_all("tr")[1:]  # Skip the headings row
    results = Results()
    for row in rows:
        row_strings = list(map(table_data_cell_transformer, row.find_all("td")))

        assert len(row_strings) == 12
        result = Result(*row_strings)
        results.append(result)

    results.page_min = page_min
    results.page_max = page_max
    results.max_num = max_count

    assert len(results) == page_max - page_min + 1

    return results


# Regex patterns


PIPE = "\|"  # Escape the pipe character

# Capture groups
NO_RESULTS = "(?P<no_results>0 files found)"

MAX_NUM = "(?P<max_num>\d+)"
PAGE_MIN = "(?P<page_min>\d+)"
PAGE_MAX = "(?P<page_max>\d+)"
RESULTS = f"{MAX_NUM} files found {PIPE} showing results from {PAGE_MIN} to {PAGE_MAX}"

PAGE_COUNT_PATTERN = re.compile(NO_RESULTS + "|" + RESULTS)

# Soup functions


def get_max_count(soup) -> int:
    """
    Extracts the maximum number of results from the search page.

    Args:
        page : Page - The search page.

    Returns:
        int: The maximum number of results.

    Example:
        [table 1]
            <td>
                <font size="1">461 files found | showing results from 451 to 461</font>
            </td>     max_num  ^^^                           page_min ^^^    ^^^ page_max

        [table 1]
        <td>
            <font size="1">0 files found</font>
        </td>              ^ max_num == page_num == 0
    """
    counts_text = soup.find_all("table")[1].find_all("td")[0].font.text
    matches = PAGE_COUNT_PATTERN.search(counts_text)
    if matches.group("no_results"):
        return 0, 0, 0

    max_num = matches.group("max_num")
    page_min = matches.group("page_min")
    page_max = matches.group("page_max")

    return int(page_min), int(page_max), int(max_num)


def strip_i_tags(soup: BeautifulSoup) -> None:
    """
    Strips the <i> tags from a soup document.

    Args:
        soup : BeautifulSoup - The soup document.

    Returns:
        None - Modifies the original document.
    """
    [i_tag.decompose() for i_tag in soup.find_all("i")]


def table_data_cell_transformer(table_data_cell: PageElement):
    """
    Extract either text or link from a results table data cell.

    Book titles have links with and empty title attribute
    Mirror links have a nonempty title attribute
    Other fields have no links

    Example"
        Extract the text from ordinary data cells:
                <td>Berkley</td>
                <td nowrap>2003</td>

        Extract the text from book title cells (has link, title is empty):
                <td><a href='search.php?req=Agatha Christie&column[]=author'>Agatha Christie</a></td>
                <td width=500><a href="search.php?req=Hercule+Poirot&column=series"></a><br><a href='book/index.php?md5=...' title='' id=...></a>The Mysterious Affair at Styles</td>

        Extract the href from mirror link cells (has link, title is nonempty):
                <td><a href='http://library.lol/main/...' title='this mirror'>[1]</a></td>
                <td><a href='http://libgen.lc/ads.php?md5=...' title='Libgen.lc'>[2]</a></td>
                <td><a href='https://library.bz/main/edit/...' title='Libgen Librarian'>[edit]</a></td>
    """

    cell_has_link_with_title = table_data_cell.a and table_data_cell.a.get("title", "")

    if cell_has_link_with_title:
        cell_link = table_data_cell.a["href"]
        return cell_link

    cell_text = "".join(table_data_cell.stripped_strings)
    return cell_text
