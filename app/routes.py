from flask import Flask, render_template, jsonify
from .database import DatabaseConnectionMessages, DatabaseConnectionAmazon
from .visualizations import DataVisualizer
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/overview-messages')
    def overview_messages():
        db = DatabaseConnectionMessages()
        tables = db.get_table_names()
        return render_template('overview-messages.html', tables=tables)
    
    @app.route('/most-popular-products')
    def get_most_popular_products():
        db = DatabaseConnectionAmazon()
        result = db.get_most_popular_products()
        
        df = pd.DataFrame(result)
        
        plt.figure(figsize=(12, 10))
        plt.bar(df["Name"], df["RatingCount"], color='skyblue')
        plt.ylim(300000, 450000)
        plt.xlabel("Product Name")
        plt.ylabel("Rating Count")
        plt.xticks(rotation=35, ha='right')
        #plt.title("Top 5 Best-Selling Products")
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart = base64.b64encode(img.getvalue()).decode('utf8')
        
        # Clearing the plot, causing crash
        #plt.close()
        
        return render_template('most-popular-products.html', chart=chart)

    return app