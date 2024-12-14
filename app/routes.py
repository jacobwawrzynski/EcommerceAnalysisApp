from flask import Flask, render_template, jsonify
from .database import DatabaseConnection
from .visualizations import DataVisualizer

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        """
        Main index page showing available database tables
        """
        db = DatabaseConnection()
        tables = db.get_table_names()
        return render_template('index.html', tables=tables)
    
    @app.route('/sales-analysis')
    def sales_analysis():
        """
        Sales analysis page with multiple visualizations
        """
        # Connect to database
        db = DatabaseConnection()
        
        # Execute complex sales analysis query
        sales_query = """
        SELECT 
            o.OrderTimestamp,
            o.Total,
            a.Category,
            a.Gender
        FROM Orders o
        JOIN OrderPositions op ON o.Id = op.OrderId
        JOIN Articles a ON op.ArticleId = a.Id
        """
        
        sales_df = db.get_dataframe(sales_query)
        
        if sales_df is not None:
            visualizer = DataVisualizer(sales_df)
            
            return render_template('charts.html', 
                sales_by_category=visualizer.sales_by_category(),
                customer_frequency=visualizer.customer_purchase_frequency(),
                monthly_sales_chart=visualizer.interactive_sales_by_month()
            )
        
        return "Error loading data", 500

    return app