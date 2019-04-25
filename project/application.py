import os
import datetime
import random

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///quiz.db")



right_answers = {}
quiztions = {}


@app.route("/")
def index():
    """main screen"""
    if not session:
        return render_template("main.html", moderator=0)

    else:
        return render_template("main.html", moderator=session["type"])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["username"]
        session["type"] = rows[0]["moderator"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":

        session.clear()

        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("must confirm the password", 400)

        row_check = db.execute("SELECT * FROM users WHERE username = :username",
                               username=request.form.get('username'))

        if not len(row_check) == 0:
            return apology("User exists", 400)

        usrname = request.form.get('username')
        pass_hash = generate_password_hash(request.form.get('password'))
        db.execute("INSERT INTO users (username, hash) VALUES (:usrname, :pass_hash)", usrname=usrname, pass_hash=pass_hash)
        user_session = db.execute("SELECT * FROM users WHERE username = :usrname", usrname=usrname)
        session["user_id"] = user_session[0]["username"]
        session["type"] = user_session[0]["moderator"]

        return redirect("/")


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    """Quiz start"""
    if request.method == "GET":
        return render_template("quiz.html")

    elif request.method == "POST":
        question_list = []
        session["difficulty"] = request.form.get("difficulty")
        if session["difficulty"] == "hard":
            question_list = db.execute("SELECT * FROM questions")

        elif session["difficulty"] == "medi":
            question_list = db.execute("SELECT * FROM questions WHERE difficulty != 'hard'")

        else:
            question_list = db.execute("SELECT * FROM questions WHERE difficulty = 'easy'")

        right_answers[session["user_id"]] = {}
        quiztions[session["user_id"]] = []

        for item in question_list:
            right_answers[session["user_id"]][item["question"]] = item["right_ans"]
            answers = [item["right_ans"], item["wrong1"], item["wrong2"], item["wrong3"]]
            random.shuffle(answers)
            answers.insert(0, item["question"])
            quiztions[session["user_id"]].append(answers)

        random.shuffle(quiztions[session["user_id"]])
        session["score"] = 0
        session["count"] = 1
        session["total"] = len(quiztions[session["user_id"]])
        return render_template("quizing.html", count=session["count"], total=session["total"], question=quiztions[session["user_id"]][0])


@app.route("/quizing", methods=["GET", "POST"])
@login_required
def quizing():
    """ Quiz middle page """
    answer = request.form.get("answer")
    if right_answers[session["user_id"]][quiztions[session["user_id"]][0][0]] == answer:
        session["score"] += 1

    quiztions[session["user_id"]].pop(0)
    session["count"] += 1
    if session["count"] > session["total"]:

        """ ADD RESULTS TO DATABASE """
        prev_res = db.execute("SELECT * FROM users WHERE username = :username", username=session["user_id"])
        if session["score"] > prev_res[0][session["difficulty"]]:
            db.execute("UPDATE users SET :difficulty = :score WHERE username = :username", username=session["user_id"], difficulty=session['difficulty'], score=session["score"])

        return render_template("result.html", score=session["score"], total=session["total"], difficulty=session["difficulty"])

    else:
        return render_template("quizing.html", count=session["count"], total=session["total"], question=quiztions[session["user_id"]][0])


@app.route("/result", methods=["GET", "POST"])
@login_required
def result():
    """ Results are here """
    if request.method == "GET":
        row = db.execute("SELECT * FROM users WHERE username = :username", username=session["user_id"])
        return render_template("results.html", row=row[0])


@app.route("/enroll", methods=["GET", "POST"])
@login_required
def enroll():
    """Show form of enrollment user"""
    if request.method == "GET":
        return render_template("enroll.html")

    elif request.method == "POST":
        if not request.form.get("contact_data"):
            return apology("must provide contact information", 400)

        db.execute("INSERT INTO registrants (time_stamp, username, course_type, contact_data, completed) VALUES (:time_stamp, :username, :course_type, :contact_data, 0)",
                   time_stamp=datetime.datetime.now(), username=session["user_id"], course_type=request.form.get("course_type"),
                   contact_data=request.form.get("contact_data"))

        return redirect("/")


@app.route("/registrants", methods=["GET"])
@login_required
def registrants():
    if not session["type"]:
        return apology("You are not welcome here", 403)

    else:
        rows = db.execute("SELECT * FROM registrants")
        return render_template("/registrants.html", rows=rows)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
