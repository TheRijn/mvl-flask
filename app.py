import os

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    result = Post.query.order_by(Post.priority).all()
    print(result)
    return render_template("main/index.html", count=12)


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


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer, unique=True, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    category = db.relationship("Category", lazy=True)

    title = db.Column(db.String(80), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)

    images = db.relationship("Image", backref="post", lazy=True)

    @property
    def serialize(self):
        return {"id": self.id,
                "priority": self.priority,
                "category_id": self.category_id,
                "category": self.category.name,
                "title": self.title,
                "intro": self.intro,
                "description": self.description,
                "images": self.images}


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(80), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

