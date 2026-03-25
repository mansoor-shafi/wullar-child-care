from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------------- DB INIT ----------------
def init_db():
    conn = sqlite3.connect('admissions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS admissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            parent_name TEXT,
            phone TEXT,
            age TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Backend Running 🚀"

# ---------------- SUBMIT ----------------
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    conn = sqlite3.connect('admissions.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO admissions (child_name, parent_name, phone, age, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['child_name'],
        data['parent_name'],
        data['phone'],
        data['age'],
        data['message']
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Form submitted successfully ✅"})

# ---------------- GET STUDENTS ----------------
@app.route("/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect('admissions.db')
    c = conn.cursor()

    c.execute("SELECT * FROM admissions")
    rows = c.fetchall()

    conn.close()

    students = []
    for row in rows:
        students.append({
            "id": row[0],
            "child_name": row[1],
            "parent_name": row[2],
            "phone": row[3],
            "age": row[4],
            "message": row[5]
        })

    return jsonify(students)

# ---------------- DELETE ----------------
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = sqlite3.connect('admissions.db')
    c = conn.cursor()

    c.execute("DELETE FROM admissions WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted successfully ✅"})

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

# ---------------- RUN APP (ALWAYS LAST) ----------------
if __name__ == "__main__":
    app.run(debug=True)