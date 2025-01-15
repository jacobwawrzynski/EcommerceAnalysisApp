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
    
    @app.route('/messages-types')
    def messages_types():
        db = DatabaseConnectionMessages()
        result = db.get_messages_types()
        
        df = pd.DataFrame(result)
        plt.figure(figsize=(15, 7))
        
        provider_counts = df['EmailProvider'].value_counts()

        provider_percentage = provider_counts / provider_counts.sum() * 100

        aggregated_counts = provider_percentage[provider_percentage >= 2]
        others_count = provider_percentage[provider_percentage < 2].sum()
        aggregated_counts['Others'] = others_count

        plt.subplot(1, 2, 1)
        aggregated_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Distribution of Email Providers')
        plt.ylabel('')
        
        # First pie chart for EmailProvider
        # plt.subplot(1, 2, 1)
        # df['EmailProvider'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        # plt.title('Distribution of Email Providers')

        plt.subplot(1, 2, 2)
        df['MessageType'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Distribution of Message Types')

        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart = base64.b64encode(img.getvalue()).decode('utf8')
        
        return render_template('messages-types.html', chart=chart)
    
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
        
        return render_template('most-popular-products.html', chart=chart)

    @app.route('/amazon-basic-statistics')
    def get_basic_statistics():
        db = DatabaseConnectionAmazon()
        result = db.get_basic_statistics()
        
        df = pd.DataFrame(result)
        
        avg_rating = df['Rating'].mean()
        avg_rating_count = df['RatingCount'].mean()
        median_rating = df['Rating'].median()
        median_rating_count = df['RatingCount'].median()
        avg_discount_perc = df['DiscountPercentage'].mean()
        median_discount_perc = df['DiscountPercentage'].median()
        
        result = {
            'avg_rating': avg_rating,
            'avg_rating_count': avg_rating_count,
            'median_rating': median_rating,
            'median_rating_count': median_rating_count,
            'avg_discount_perc': avg_discount_perc,
            'median_discount_perc': median_discount_perc
        }
        
        return render_template('amazon-basic-statistics.html', result=result)

    return app