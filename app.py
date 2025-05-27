import datetime
from dotenv import load_dotenv
from flask import Flask, abort, render_template, request
import os

load_dotenv()
app = Flask(__name__)

state = {"status": None, "status_since": None, "last_updated": datetime.datetime.now()}


@app.template_filter()
def map_status(status):
    if status == "free":
        return "Available"
    elif status == "call":
        return "In a call"
    return "Unknown"


@app.template_filter()
def format_datetime(timestamp):
    if timestamp is None:
        return "Unknown"
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


@app.route("/")
def index():
    return render_template("index.html", **state)


@app.route("/update", methods=["POST"])
def update():
    data = request.json
    if "API_SECRET" not in data or data["API_SECRET"] != os.environ["API_SECRET"]:
        abort(401)  # unauthorized
    if data["status"] not in ("call", "free"):
        abort(400)  # bad request
    state["status"] = data["status"]
    state["status_since"] = datetime.datetime.fromisoformat(data["status_since"])
    state["last_updated"] = datetime.datetime.now()
    return state
