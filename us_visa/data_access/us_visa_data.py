import sys
import pandas as pd
import numpy as np
from us_visa.exception import USvisaException
from us_visa.configuration.snowflake_connection import SnowflakeClient


class USvisaData:
    """
    This class helps to export Snowflake query results as pandas dataframe
    """

    def __init__(self):
        try:
            self.snowflake_client = SnowflakeClient()
        except Exception as e:
            raise USvisaException(e, sys)

    def export_collection_as_dataframe(self, query: str) -> pd.DataFrame:
        """
        Execute query and return result as pandas DataFrame
        """
        try:
            # Use Pandas read_sql for direct DataFrame fetch
            df = pd.read_sql(query, self.snowflake_client.client)
            # Replace "na" string values with np.nan
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise USvisaException(e, sys)
