from flask import Flask, request
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="appuser",
        password="apppassword",
        database="monitoring"
    )


@app.route("/")
def home():

    connection = get_db_connection()
    cursor = connection.cursor()

    ip_address = request.remote_addr

    cursor.execute(
        "INSERT INTO visitors (ip_address) VALUES (%s)",
        (ip_address,)
    )

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM visitors")
    visitor_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return f"""
    <html>
        <head>
            <title>IT Monitoring Dashboard</title>
        </head>

        <body>
            <h1>IT Monitoring Dashboard - CI/CD TEST</h1>

            <h2>Server Status</h2>

            <p>Server: Production-Web-01</p>
            <p>Status: Online</p>
            <p>CPU: 35%</p>
            <p>RAM: 62%</p>

            <h2>Visitors</h2>

            <p>Website Visitors: {visitor_count}</p>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)