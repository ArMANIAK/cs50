import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("SELECT * FROM users_stocks WHERE user_id = :user_id", user_id=session['user_id'])
    cash = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session['user_id'])
    money = cash[0]['cash']
    total_cash = money

    cur_cost = []
    price = []

    for row in rows:
        actual_price = lookup(row['stock_id'])
        price.append(actual_price['price'])
        cur_cost.append(actual_price['price'] * row['quantity'])
        total_cash += actual_price['price'] * row['quantity']

    return render_template("stocks.html", prices=zip(rows, cur_cost, price), total_cash=total_cash, money=money)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        try:
            shares_quantity = int(request.form.get('shares'))
            if shares_quantity <= 0:
                return apology("Shares should be a positive number")

        except ValueError:
            return apology("Shares should be a positive number")

        stock_id = request.form.get('symbol')
        result = lookup(stock_id)
        if not result:
            return apology("Wrong stock symbol", 400)

        cash = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session['user_id'])

        # decide how to get cash out of 'cash'

        if cash[0]['cash'] < shares_quantity * result['price']:
            return apology("Not enough money")

        else:

            # add to history, add to portfolio

            time_stamp = datetime.datetime.now()

            row = db.execute("SELECT * FROM users_stocks WHERE user_id = :user_id AND stock_id = :stock_id",
                             user_id=session['user_id'], stock_id=stock_id)
            if row:
                db.execute("UPDATE users_stocks SET quantity = :new_quantity WHERE user_id = :user_id AND stock_id = :stock_id",
                           user_id=session['user_id'], stock_id=stock_id, new_quantity=shares_quantity + row[0]['quantity'])

            else:
                db.execute("INSERT INTO users_stocks (user_id, stock_id, quantity) VALUES (:user_id, :stock_id, :quantity)",
                           user_id=session['user_id'], stock_id=stock_id, quantity=shares_quantity)

            db.execute("INSERT INTO purchase_history (stock_id, quantity, actual_price, time, sold) VALUES (:stock_id, :quantity, :price, :time_stamp, 'False')",
                       stock_id=stock_id, quantity=shares_quantity, price=result['price'], time_stamp=time_stamp)
            db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id",
                       new_cash=cash[0]['cash'] - shares_quantity * result['price'], user_id=session['user_id'])
        return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    q = request.args.get("username")
    usernames = db.execute("SELECT * FROM users WHERE username = :username", username=q)

    return jsonify(not usernames)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute("SELECT * FROM purchase_history")
    for row in rows:
        if row['sold']:
            row['sold'] = "Bought"

        else:
            row['sold'] = "Sold"

    return render_template("history.html", rows=rows)


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
        session["user_id"] = rows[0]["id"]

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("get_quote.html")

    else:
        result = lookup(request.form.get('symbol'))
        if not result:
            return apology("No such ticker symbol", 400)
        return render_template("quoted.html", result=result)


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
        session["user_id"] = user_session[0]["id"]

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        rows = db.execute("SELECT stock_id, quantity FROM users_stocks WHERE user_id = :user_id", user_id=session['user_id'])
        if not rows:
            return apology("You have no shares for now")

        else:
            return render_template("sell.html", rows=rows)

    else:
        try:
            shares_quantity = int(request.form.get('shares'))
            if shares_quantity <= 0:
                return apology("Shares should be a positive number")

        except ValueError:
            return apology("Shares should be a positive number")

        stock_id = request.form.get('symbol')
        result = lookup(stock_id)
        cash = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session['user_id'])
        rows = db.execute("SELECT * FROM users_stocks WHERE user_id = :user_id AND stock_id = :symbol",
                          user_id=session['user_id'], symbol=stock_id)
        if rows[0]['quantity'] < shares_quantity:
            return apology("You don't have that many shares")

        elif rows[0]['quantity'] == shares_quantity:
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                       cash=cash[0]['cash'] + rows[0]['quantity'] * result['price'], user_id=session['user_id'])
            db.execute("DELETE FROM users_stocks WHERE user_id = :user_id AND stock_id = :symbol",
                       user_id=session['user_id'], symbol=stock_id)

        else:
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash[0]['cash'] + shares_quantity * result['price'],
                       user_id=session['user_id'])
            db.execute("UPDATE users_stocks SET quantity = :quantity WHERE user_id = :user_id AND stock_id = :symbol",
                       user_id=session['user_id'], symbol=stock_id, quantity=rows[0]['quantity'] - shares_quantity)

        time_stamp = datetime.datetime.now()
        db.execute("INSERT INTO purchase_history (stock_id, quantity, actual_price, time, sold) VALUES (:stock_id, :quantity, :price, :time_stamp, 'True')",
                   stock_id=stock_id, quantity=shares_quantity, price=result['price'], time_stamp=time_stamp)
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
