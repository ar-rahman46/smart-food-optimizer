from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("food.db")

def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS food (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            calories INTEGER,
            date TEXT
        )
    """)
    db.commit()
    db.close()

init_db()

# ---------- ADD FOOD ----------
@app.route("/add", methods=["GET", "POST"])
def add_food():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        calories = request.form["calories"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO food (name, price, calories, date) VALUES (?, ?, ?, date('now'))",
            (name, price, calories)
        )
        db.commit()
        db.close()

        return redirect("/add")

    return render_template("add_food.html")

# ---------- SUMMARY ----------
@app.route("/summary")
def summary():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT SUM(price), SUM(calories) FROM food WHERE date = date('now')")
    data = cur.fetchone()

    total_price = data[0] if data[0] else 0
    total_calories = data[1] if data[1] else 0

    if total_calories > 2500:
        suggestion = "High calories today. Eat light tomorrow."
    elif total_price > 300:
        suggestion = "High spending today. Try budget food."
    else:
        suggestion = "Great balance! Keep it up 👍"

    return render_template(
        "summary.html",
        total_price=total_price,
        total_calories=total_calories,
        suggestion=suggestion
    )

# ---------- HOME ----------
@app.route("/")
def home():
    return "Database connected successfully!"

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
