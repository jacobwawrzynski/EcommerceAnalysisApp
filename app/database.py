#<antArtifact identifier="database-connection" type="application/vnd.ant.code" language="python" title="Database Connection Module">
import pyodbc
import pandas as pd
from sqlalchemy import create_engine
import urllib

class DatabaseConnection:
    def __init__(self, server='localhost', database='e_commerce'):
        # Connection string for SQL Server using pyodbc
        params = urllib.parse.quote_plus(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            'Trusted_Connection=yes;'
        )
        
        # SQLAlchemy engine
        self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    def get_dataframe(self, query):
        """
        Execute SQL query and return as pandas DataFrame
        
        Args:
            query (str): SQL query to execute
        
        Returns:
            pd.DataFrame: Result of the query
        """
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def get_table_names(self):
        """
        Retrieve all table names in the database
        
        Returns:
            list: Table names
        """
        query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        """
        tables = pd.read_sql(query, self.engine)
        return tables['TABLE_NAME'].tolist()