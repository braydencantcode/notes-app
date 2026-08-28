from flask import Flask, render_template, request, jsonify, redirect, url_for, session
app = Flask(__name__)

notes = []

import sqlite3 

def get_db_connection(): # this basically opens connection with the database . cool
    connection = sqlite3.connect("notes.db")
    connection.row_factory = sqlite3.Row  
    return connection 

def init_db(): 
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    connection.execute("""CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
    )""")
    connection.commit()
    connection.close()

init_db() # initialise/create database

def username_exists(username):
    connection = get_db_connection()
    user = connection.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    connection.close()
    return user is not None

app.secret_key = "change-later"

@app.route("/")
def index():
    if not session.get("logged in"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/notes", methods=["GET"])
def get_notes():
    user_id = session.get("user_id")
    connection = get_db_connection()
    your_notes = connection.execute("SELECT text FROM notes WHERE user_id = ?", (user_id,)).fetchall()
    connection.close()
    notes_list = [row["text"] for row in your_notes]
    return jsonify(notes_list)

@app.route("/notes", methods=["POST"])
def add_note():
    user_id = session.get("user_id")
    data = request.get_json()
    text = data.get("text", "")

    connection = get_db_connection()
    connection.execute(
        "INSERT INTO notes (user_id, text) VALUES (?, ?)",
        (user_id, text)
    )
    connection.commit()
    connection.close()
    return jsonify({"success": True}), 201

@app.route("/notes", methods=["DELETE"])
def clear_notes():
    user_id = session.get("user_id")
    connection = get_db_connection()
    connection.execute("DELETE FROM notes WHERE user_id = ?", (user_id,))
    connection.commit()
    connection.close()
    return jsonify({"success": True}), 200

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip().casefold()
        password = request.form.get("password")

        connection = get_db_connection()
        user = connection.execute(
            "SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        connection.commit()
        connection.close()

        if user is not None and user["password"] == password:
            session["logged in"] = True
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Wrong username or password")
        
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("logged in", None)
    return redirect(url_for("login"))

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username", "").strip().casefold()
    password = data.get("password", "")

    if username_exists(username):
        return jsonify({"error": "Username already taken"}), 409

    connection = get_db_connection()
    connection.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    connection.commit()
    connection.close()

    print(f"successful account creation with username: {username} and password: {password}") # this line is for debugging
    return jsonify({"success": True}), 201
    
@app.route("/whoami")
def whoami():
    if not session.get("logged in"):
        return jsonify({"username": None}), 401
    return jsonify({"username": session.get("username")})

if __name__ == "__main__":
    app.run(debug=True)