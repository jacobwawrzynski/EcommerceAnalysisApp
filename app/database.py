#<antArtifact identifier="database-connection" type="application/vnd.ant.code" language="python" title="Database Connection Module">
import pyodbc
import pandas as pd
from sqlalchemy import create_engine
import urllib

class DatabaseConnectionMessages:
    def __init__(self, server='localhost', database='e_commerce'):
        params = urllib.parse.quote_plus(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            'Trusted_Connection=yes;'
        )
        
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
        query = """
        SELECT
        t.TABLE_NAME AS entity_name,
        CONVERT(VARCHAR(20), p.rows) AS records,
        td.description AS description
        FROM 
        INFORMATION_SCHEMA.TABLES t
        LEFT JOIN 
        sys.tables st ON t.TABLE_NAME = st.name
        LEFT JOIN 
        sys.partitions p ON st.object_id = p.object_id 
        AND p.index_id IN (0, 1)
        LEFT JOIN 
        sys.extended_properties ep ON st.object_id = ep.major_id 
        AND ep.minor_id = 0 
        AND ep.name = 'MS_Description'
        JOIN 
        tables_description td on td.name=t.TABLE_NAME
        """
        tables = pd.read_sql(query, self.engine)
        return tables.to_dict(orient='records')

class DatabaseConnectionAmazon:
    def __init__(self, server='localhost', database='amazon_data'):
        params = urllib.parse.quote_plus(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            'Trusted_Connection=yes;'
        )
        
        self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    def get_table_names(self):
        query = """
        SELECT
        t.TABLE_NAME AS entity_name,
        CONVERT(VARCHAR(20), p.rows) AS records,
        'not available' AS description
        FROM 
        INFORMATION_SCHEMA.TABLES t
        LEFT JOIN 
        sys.tables st ON t.TABLE_NAME = st.name
        LEFT JOIN 
        sys.partitions p ON st.object_id = p.object_id 
        AND p.index_id IN (0, 1)
        LEFT JOIN 
        sys.extended_properties ep ON st.object_id = ep.major_id 
        AND ep.minor_id = 0 
        AND ep.name = 'MS_Description'
        """
        tables = pd.read_sql(query, self.engine)
        return tables.to_dict(orient='records')
        