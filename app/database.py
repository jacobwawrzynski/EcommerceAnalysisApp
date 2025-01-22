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
    
    def get_messages_types(self):
        query = """
        select top(10000) 
		Email_provider as EmailProvider
		,Message_type as MessageType
		from Messages
        """
        result = pd.read_sql(query, self.engine)
        return result.to_dict()

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
    
    def get_most_popular_products(self):
        query = """
        select TOP(10)
        Product_id as Product
        ,Product_name as Name
        ,CONVERT(INT, Rating) as Rating
        ,CONVERT(INT, Rating_count) as RatingCount
        from Sales
        group by Product_id
        ,Product_name
        ,Rating_count
        ,Rating
        having COUNT(Rating_count) = 1
        order by CONVERT(INT, Rating_count) desc
        """
        result = pd.read_sql(query, self.engine)
        return result.to_dict()
    
    def get_basic_statistics(self):
        query = """
        select CONVERT(INT,Discounted_price) as DiscountPrice
		,CONVERT(INT,Actual_price) as ActualPrice
		,CONVERT(INT,Discount_percentage) as DiscountPercentage
		,CONVERT(INT,Rating) as Rating
		,CONVERT(INT,Rating_count) as RatingCount
		from Sales
        """
        result = pd.read_sql(query, self.engine)
        return result.to_dict()
    
    def get_best_reviews(self):
        query = """
        select top(10) Review_title as Review
        from Sales
        where Product_id in (
        select Product_id
        from Sales
        where convert(int,Rating) > 40 
        )
        """
        result = pd.read_sql(query, self.engine)
        return result.to_dict(orient='records')
    
    def get_price_differences(self):
        query = """
        select top(10) 
        Product_name as Name
        ,Discount_percentage as DiscountPercentage
        ,(cast(Actual_price as int) - cast(Discounted_price as int)) as PriceDifference
        from Sales
        order by PriceDifference desc
        """
        result = pd.read_sql(query, self.engine)
        return result.to_dict()