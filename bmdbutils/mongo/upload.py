"""
Upload utilities
"""
import pandas as pd
import pymongo


def upload_table(
    df: pd.DataFrame,
    collection: pymongo.collection.Collection,
    **kwargs
) -> pd.Series:
    """
    Uploads a DataFrame to a MongoDB collection.

    Parameters
    ----------
    df
    collection
    kwargs

    Returns
    -------
    Series with inserted documents IDs.
    """
    documents = df.to_dict("records")
    result = collection.insert_many(documents, kwargs)

    return pd.Series(result.inserted_ids)
