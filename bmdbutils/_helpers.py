"""
General helper functions.
"""

from datetime import date, timedelta


def clean_date_range(init_date=None, end_date=date.today()):
    """
    Given two objects return valid initial and end dates ready to be used in queries

    Parameters
    ----------
    init_date : datetime
                Proposed initial datetime
    end_date : datetime
                Proposed initial datetime

    Returns
    -------
    list
        initial and end dates
    """
    end_date = end_date.date()
    if not init_date:
        init_date = end_date - timedelta(days=30)
    else:
        init_date = init_date.date()

    return (init_date, end_date)


def clean_tax_list(tax_ids=list()):
    """
    Create valid tax ids list from an input string

    Parameters
    ----------
    tax_ids : str
              raw tax id list

    Returns
    -------
    list
        list of valid tax ids
    """
    clean_list = list(
        map(lambda id: id.strip().replace(' ', ''), tax_ids.split(',')))
    tax_list = filter(lambda id: int(id), clean_list)
    return tax_list
