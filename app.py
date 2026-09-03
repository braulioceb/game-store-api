from flask import Flask
from db.conn import open_connection 
from db.utils import get_df
import pandas as pd


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <p>Video Game Store and entertainment articles</p>
    </body>
    </html>
    """

@app.route("/reports", methods=["GET"])
def reports_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <h2>Reports</h2>
        <p>General reports Game Store. </p>
    </body>
    </html>
    """

@app.route("/reports/sales", methods=["GET"])
def sales_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <h2>Sales Reports</h2>
        <p>Reports for sales</p>
    </body>
    </html>
    """

@app.route("/reports/sales/<fecha>", methods=["GET"])
def sales_month_page(fecha):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <h2>Sales Reports</h2>
        <p>Reports for sales: {fecha} </p>
    </body>
    </html>
    """

@app.route("/reports/sales/hist", methods=["GET"])
def sales_hist_page():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <h2>Sales Reports</h2>
        <p>Reports for sales Historia </p>
        <table border="1" id="salesTable">
            <thead>
                <tr>
                    <th>Month Example</th>
                    <th>Import Example</th>
                </tr>
            </thead>
            <tbody id="salesTableBody">
                <tr>
                    <th>2026-05</th>
                    <th>10,000</th>
                </tr>
                <tr>
                    <th>2026-04</th>
                    <th>12,000</th>
                </tr>
            </tbody>
        </table>

    </body>
    </html>
    """

@app.route("/api/sales/reports/hist", methods=["GET"])
def sales_rp_hist():
    conn = open_connection()

    query = """SELECT 
	    LAST_DAY(purchase_date) as month,
        SUM(import) as import
    FROM game_store.sales
    GROUP BY LAST_DAY(purchase_date);"""

    # datetime to format data: YYYY-MM-DD. Example 2026-03-02
    df_rp_hist = get_df(conn, query)
    df_rp_hist["month"]= pd.to_datetime(df_rp_hist["month"]).dt.strftime("%Y-%m-%d")

    return df_rp_hist.values.tolist()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)