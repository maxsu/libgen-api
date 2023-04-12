from operator import attrgetter
from .result import Result


class Results(list[Result]):
    page_min: int
    page_max: int
    max_num: int

    def filter(self, filters, exact_match=True):
        """
        Returns a list of results that match the given filter criteria.
        When exact_match = true, we only include results that exactly match
        the filters (ie. the filters are an exact subset of the result).

        When exact-match = false,
        we run a case-insensitive check between each filter field and each result.

        exact_match defaults to TRUE -
        this is to maintain consistency with older versions of this library.
        """

        filtered_results = []
        if exact_match:
            # check whether a candidate result matches the given filters
            filtered_results = [r for r in self if filters.items() <= r.asdict().items()]

        else:
            for result in self:
                if not result:
                    continue

                if all(
                    value.casefold() in attrgetter(key.lower())(result).casefold()
                    for key, value in filters.items()
                ):
                    filtered_results.append(result)

        return filtered_results
