from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "submissions.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name TEXT,
        q1 TEXT,
        q2 TEXT,
        q3 TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return "RefactorX Backend Running"


@app.route("/submit", methods=["POST"])
def submit():

    data = request.json

    team = data.get("team_name")
    q1 = data.get("q1")
    q2 = data.get("q2")
    q3 = data.get("q3")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO submissions (team_name,q1,q2,q3) VALUES (?,?,?,?)",
        (team, q1, q2, q3)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})


@app.route("/submissions")
def submissions():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT team_name,q1,q2,q3,timestamp FROM submissions")

    rows = cursor.fetchall()

    conn.close()

    result = []

    for r in rows:
        result.append({
            "team": r[0],
            "q1": r[1],
            "q2": r[2],
            "q3": r[3],
            "time": r[4]
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
