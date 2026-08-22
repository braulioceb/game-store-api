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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)