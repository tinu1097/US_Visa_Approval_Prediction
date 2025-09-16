import sys
import os
from dotenv import load_dotenv
from snowflake.connector import connect, DictCursor
from us_visa.exception import USvisaException
from us_visa.logger import logging

# Load credentials
load_dotenv()

class SnowflakeClient:
    """
    Class for managing Snowflake connection and queries.
    """

    client = None

    def __init__(self) -> None:
        try:
            if SnowflakeClient.client is None:
                SnowflakeClient.client = connect(
                    user=os.getenv("SNOWFLAKE_USER"),
                    password=os.getenv("SNOWFLAKE_PASSWORD"),
                    account=os.getenv("SNOWFLAKE_ACCOUNT"),
                    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                    database=os.getenv("SNOWFLAKE_DATABASE"),
                    schema=os.getenv("SNOWFLAKE_SCHEMA"),
                    role=os.getenv("SNOWFLAKE_ROLE"),
                )
            self.client = SnowflakeClient.client
            logging.info("✅ Snowflake connection successful")
        except Exception as e:
            raise USvisaException(e, sys)

    def fetch_data(self, query: str):
        """
        Execute SELECT query and return results as list of dicts.
        """
        try:
            cur = self.client.cursor(DictCursor)
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            raise USvisaException(e, sys)
        finally:
            cur.close()

    # def execute_query(self, query: str):
    #     """
    #     Execute non-SELECT query (INSERT/UPDATE/DELETE).
    #     """
    #     try:
    #         cur = self.client.cursor()
    #         cur.execute(query)
    #         self.client.commit()
    #         logging.info("✅ Query executed successfully")
    #     except Exception as e:
    #         raise USvisaException(e, sys)
    #     finally:
    #         cur.close()
