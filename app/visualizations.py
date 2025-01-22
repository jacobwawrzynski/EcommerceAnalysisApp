import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

class DataVisualizer:
    def __init__(self, dataframe):
        self.df = dataframe

    def sales_by_category(self):
        plt.figure(figsize=(10, 6))
        sales_by_category = self.df.groupby('Category')['Total'].sum().sort_values(ascending=False)
        sales_by_category.plot(kind='bar')
        plt.title('Total Sales by Product Category')
        plt.xlabel('Category')
        plt.ylabel('Total Sales')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return self._plt_to_base64()

    def customer_purchase_frequency(self):
        plt.figure(figsize=(10, 6))
        purchase_counts = self.df['CustomerId'].value_counts()
        purchase_counts.plot(kind='hist', bins=10)
        plt.title('Customer Purchase Frequency')
        plt.xlabel('Number of Purchases')
        plt.ylabel('Number of Customers')
        plt.tight_layout()
        
        return self._plt_to_base64()

    def interactive_sales_by_month(self):
        # Convert OrderTimestamp to datetime
        self.df['OrderMonth'] = pd.to_datetime(self.df['OrderTimestamp']).dt.to_period('M')
        monthly_sales = self.df.groupby('OrderMonth')['Total'].sum().reset_index()
        
        fig = px.line(
            monthly_sales, 
            x='OrderMonth', 
            y='Total', 
            title='Monthly Sales Trend',
            labels={'Total': 'Sales Amount', 'OrderMonth': 'Month'}
        )
        
        return fig.to_json()

    def _plt_to_base64(self):
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png).decode('utf-8')
        return graphic