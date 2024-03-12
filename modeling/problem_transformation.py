import pandas as pd


def agg_columns(multiples_columns):
    agg_columns = pd.DataFrame()
    agg_columns["Class"] = multiples_columns.astype(str).agg(''.join, axis=1)
    agg_columns["Class"] = agg_columns["Class"].astype(str)
    return agg_columns