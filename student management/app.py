from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database
conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()


# Create students table
conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rollno TEXT
)
""")

conn.commit()
conn.close()

# Registration Page
@app.route("/", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        # Validation
        if username == "" or email == "" or password == "" or confirm == "":
            return "Please fill all fields"

        if password != confirm:
            return "Password does not match"

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO users(username,email,password) VALUES(?,?,?)",
                    (username, email, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                    (username, password))

        user = cur.fetchone()

        conn.close()

        if user:
            return redirect("/dashboard")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# Add Student
@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        name = request.form["name"]
        rollno = request.form["rollno"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO students(name, rollno) VALUES(?, ?)",
                    (name, rollno))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_student.html")
@app.route("/view")
def view():

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")

    students = cur.fetchall()

    conn.close()

    return render_template("view_student.html", students=students)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        rollno = request.form["rollno"]

        cur.execute("UPDATE students SET name=?, rollno=? WHERE id=?",
                    (name, rollno, id))

        conn.commit()
        conn.close()

        return redirect("/view")

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/view")
app.run(debug=True)