"""
MongoDB submodule helper functions.
"""
import pandas as pd
import pymongo


def get_consecutive(
    collection: pymongo.collection.Collection, field: str, n: int
) -> pd.Series:
    """

    Parameters
    ----------
    collection
    field
    n

    Returns
    -------

    """
    field_max = collection.find_one(sort=[(field, pymongo.DESCENDING)]).get(field)
    sequence = range(field_max, field_max + n)

    return pd.Series(sequence) + 1


def get_difference(
    collection: pymongo.collection.Collection, field: str, values: pd.Series
) -> pd.Series:
    """

    Parameters
    ----------
    collection
    field
    values

    Returns
    -------

    """
    cursor = collection.find({field: {"$in": values}})
    intersection = [document.get(field) for document in cursor]
    difference = set(values) - set(intersection)

    return pd.Series(list(difference))
