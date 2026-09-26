import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("gsindex.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/activity", methods=["GET", "POST"])
def activity():

    print("Activity page opened")

    if request.method == "POST":
        print("REGISTER BUTTON CLICKED")

        activity_name = request.form["activity"]
        description = request.form["description"]
        date = request.form["date"]

        print(activity_name, description, date)

        conn = sqlite3.connect("greenstride.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO activities (activity_name, description, date) VALUES (?, ?, ?)",
            (activity_name, description, date)
        )

        conn.commit()
        conn.close()

        return redirect("/activity")

    conn = sqlite3.connect("greenstride.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM activities ORDER BY id DESC")
    activities = cursor.fetchall()

    conn.close()

    return render_template("activity.html", activities=activities)


@app.route("/delete/<int:id>")
def delete_activity(id):

    conn = sqlite3.connect("greenstride.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM activities WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/activity")


@app.route("/leaderboard")
def leaderboard():

    conn = sqlite3.connect("greenstride.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT activity_name, COUNT(*) as total
        FROM activities
        GROUP BY activity_name
        ORDER BY total DESC
    """)

    leaderboard_data = cursor.fetchall()

    conn.close()

    return render_template(
        "leaderboard.html",
        leaderboard_data=leaderboard_data
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("greenstride.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("greenstride.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/impact")
def impact():

    conn = sqlite3.connect("greenstride.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM activities")
    total_activities = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "impact.html",
        total_activities=total_activities,
        total_users=total_users
    )


@app.route("/suggestions")
def suggestions():
    return render_template("suggestions.html")


@app.route("/inspiration")
def inspiration():
    return render_template("inspiration.html")


if __name__ == "__main__":
    app.run(debug=True)