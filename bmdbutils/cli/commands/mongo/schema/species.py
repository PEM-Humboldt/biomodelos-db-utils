"""
MongoDB species collection schema.
"""
import pandas as pd

fields = {"acceptedNameUsage": {"type": str, "required": True, "default": pd.NA}}
