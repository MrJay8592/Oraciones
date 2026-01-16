from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "requests.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0
            )
        """)

@app.route("/")
def index():
    with sqlite3.connect(DB) as conn:
        items = conn.execute("SELECT * FROM requests").fetchall()
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    text = request.form["text"]
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO requests (text) VALUES (?)", (text,))
    return redirect("/")

@app.route("/toggle/<int:item_id>")
def toggle(item_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("UPDATE requests SET done = 1 - done WHERE id = ?", (item_id,))
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
