import os
import snowflake.connector
from django.conf import settings
import pandas as pd
from datetime import datetime, timedelta

def get_snowflake_connection():
    """Create and return a Snowflake connection using settings."""
    return snowflake.connector.connect(
        account=settings.SNOWFLAKE['account'],
        user=settings.SNOWFLAKE['user'],
        password=settings.SNOWFLAKE['password'],
        database=settings.SNOWFLAKE['database'],
        warehouse=settings.SNOWFLAKE['warehouse']
    )

def fetch_stock_data(symbol, start_date=None, end_date=None):
    """
    Fetch stock data from Snowflake for a given symbol and date range.
    Returns a pandas DataFrame with the results.
    """
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    query = f"""
    SELECT 
        date,
        open_price,
        high_price,
        low_price,
        close_price,
        volume
    FROM stock_prices
    WHERE symbol = '{symbol}'
    AND date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY date
    """

    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        return df
    except Exception as e:
        print(f"Error fetching stock data: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

def calculate_portfolio_metrics(portfolio_id):
    """
    Calculate portfolio metrics using Snowflake.
    Returns a dictionary with various portfolio statistics.
    """
    query = f"""
    WITH portfolio_data AS (
        SELECT 
            ps.portfolio_id,
            ps.stock_id,
            ps.shares,
            ps.average_price,
            sp.close_price,
            sp.date
        FROM portfolio_stocks ps
        JOIN stock_prices sp ON ps.stock_id = sp.stock_id
        WHERE ps.portfolio_id = {portfolio_id}
        AND sp.date = CURRENT_DATE()
    )
    SELECT 
        SUM(shares * close_price) as total_value,
        SUM(shares * (close_price - average_price)) as total_gain_loss,
        COUNT(DISTINCT stock_id) as number_of_stocks
    FROM portfolio_data
    """

    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        return {
            'total_value': result[0],
            'total_gain_loss': result[1],
            'number_of_stocks': result[2]
        }
    except Exception as e:
        print(f"Error calculating portfolio metrics: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.close() 