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
    return jsonify(notes)

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    text = data.get("text", "")
    notes.insert(0, text)
    return jsonify({"success": True}), 201

@app.route("/notes", methods=["DELETE"])
def clear_notes():
    notes.clear()
    return jsonify({"success": True}), 200

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # fill in later

    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("logged in", None)
    return redirect(url_for("login"))

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username", "")
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
    

if __name__ == "__main__":
    app.run(debug=True)