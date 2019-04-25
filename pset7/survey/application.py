import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

registered = []


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():

    # TODO
    name = request.form.get("name")
    age = request.form.get("age-group")
    phone = request.form.get("phone")
    if not name or not age or not phone:
        return render_template("error.html", message="All fields are required!")
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((name, age, phone, request.form.get("course")))
    file.close()
    return render_template("sheet.html")


@app.route("/sheet", methods=["GET"])
def get_sheet():

    # TODO
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    registered = list(reader)
    return render_template("sheet.html", registered=registered)
