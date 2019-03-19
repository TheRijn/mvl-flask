import os

from flask import Flask, render_template, jsonify, abort
from sqlalchemy import func

from model import Post, Category, db

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db.init_app(app)

@app.route("/")
def index():
    posts = Post.get_posts()
    return render_template("main/index.html", posts=posts)


@app.route('/<string:category_name>')
def category(category_name):

    category_item = Category.query.filter(func.lower(Category.name) == category_name.replace('_', ' ')).first()
    if not category_item:
        return abort(404)

    posts = Post.get_posts_with_category(category_item.id)

    return render_template("main/index.html", posts=posts)


@app.route("/api/post/<int:post_id>", methods=["POST"])
def get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify({"success": True, "post": post.serialize})
    else:
        return jsonify({"success": False})


@app.route("/login", methods=["GET"])
def login():
    return render_template("adm/login.html")


