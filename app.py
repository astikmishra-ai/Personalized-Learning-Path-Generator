from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)
#Home
@app.route("/")
def home():
    return render_template("index.html")
#Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return "<h2>Login Successful!</h2><a href='/dashboard'>Go to Dashboard</a>"
        else:
            return "<h2>Invalid Email or Password</h2><a href='/login'>Try Again</a>"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return """
    <h1>Student Dashboard</h1>

    <h3>Welcome to Personalized Learning Path Generator</h3>

    <ul>
        <li><a href="/quiz">Take Diagnostic Quiz</a></li>
        <li><a href="/learning-path">View Learning Path</a></li>
        <li><a href="/progress">Track Progress</a></li>
    </ul>
    """
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/result", methods=["POST"])
def result():

    python_marks = int(request.form["python"])
    dbms_marks = int(request.form["dbms"])
    dsa_marks = int(request.form["dsa"])

    average = (python_marks + dbms_marks + dsa_marks) / 3

    if average >= 80:
        level = "Advanced"
        recommendation = [
            "Solve advanced DSA problems",
            "Build Flask projects",
            "Learn Machine Learning",
            "Practice competitive programming"
        ]

    elif average >= 50:
        level = "Intermediate"
        recommendation = [
            "Revise Python fundamentals",
            "Practice DBMS SQL queries",
            "Solve basic DSA questions",
            "Watch tutorial videos"
        ]

    else:
        level = "Beginner"
        recommendation = [
            "Learn Python basics",
            "Study DBMS concepts",
            "Practice simple programs",
            "Take quizzes regularly"
        ]

    return render_template(
        "result.html",
        level=level,
        average=average,
        recommendation=recommendation
    )
@app.route("/learning-path")
def learning_path():
    return render_template(
        "result.html",
        level="Intermediate",
        average=65,
        recommendation=[
            "Revise Python Fundamentals",
            "Practice DBMS SQL Queries",
            "Solve DSA Problems Daily",
            "Watch Machine Learning Tutorials"
        ]
    )

@app.route("/progress")
def progress():
    return render_template("progress.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students(name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return "<h2>Registration Successful!</h2><a href='/login'>Go to Login</a>"
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)