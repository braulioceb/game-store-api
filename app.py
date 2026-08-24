from flask import Flask

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
def sales_date_page(fecha):
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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)