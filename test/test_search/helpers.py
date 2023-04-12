from operator import attrgetter

from libgen_api.models import Result


class Filters:
    year_extension = {"year": "2007", "extension": "epub"}
    inexact = {"extension": "PDF"}
    inexact2 = {"ExTeNsIon": "PDF"}
    exact = {"extension": "pdf"}
    partial_exact = {"extension": "p", "year": "200"}
    partial_inexact = {"extension": "p", "Year": "200"}


def fields_match(filter: dict[str, str], result: Result, exact=True):
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

    items = filter.items()

    if exact:
        return all(attrgetter(key)(result) == value for key, value in items)

    return all(value.lower() in attrgetter(key.lower())(result).lower() for key, value in items)
