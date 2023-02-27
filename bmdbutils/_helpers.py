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
        map(lambda id: id.replace(' ', ''), tax_ids.split(',')))

    def is_int(num):
        try:
            int(num)
            return True
        except:
            return False
    tax_list = filter(is_int, clean_list)
    return tax_list


def clean_str(raw_str=""):
    """
    Clean special character for some strings

    Parameters
    ----------
    raw_str : str
              raw string

    Returns
    -------
    str
        string without some characters
    """
    return raw_str.replace(':', '').replace('.', '').replace(' ', '').replace('%', '')
