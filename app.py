from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return count(12)


@app.route("/<int:item_count>")
def count(item_count):
    return render_template("index.html", count=item_count)
