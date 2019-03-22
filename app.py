import os

from flask import Flask, render_template, jsonify, abort, send_file, request, redirect, flash
from sqlalchemy import func
from base64 import standard_b64decode, standard_b64encode
from io import BytesIO

from model import db, Post, Category, ImageBase64

# Check for environment variable
env_vars = ["DATABASE_URL", "PASSWORD", 'SECRET_KEY']
for env_var in env_vars:
    if not os.getenv(env_var):
        raise RuntimeError(f"{env_var} is not set")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.getenv('SECRET_KEY')

# Bind db to application
db.init_app(app)


@app.route("/")
def index():
    posts = Post.get_posts()
    print(posts[0].title)
    return render_template("main/index.html", posts=posts)


@app.route('/<string:category_name>')
def category(category_name):
    category_item = Category.query.filter(func.lower(Category.name) == category_name.replace('_', ' ')).first()
    if not category_item:
        return abort(404)

    posts = Post.get_posts_with_category(category_item.id)

    return render_template("main/index.html", posts=posts)


@app.route('/contact')
def contact():
    return render_template("main/contact.html")


@app.route("/api/post/<int:post_id>", methods=["POST"])
def get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify({"success": True, "post": post.serialize})
    else:
        return jsonify({"success": False})


@app.route('/images/<string:filename>')
def get_image(filename):
    image_b64 = ImageBase64.query.filter(ImageBase64.filename == filename).first()
    if not image_b64:
        return abort(404)
    image = standard_b64decode(image_b64.data)
    return send_file(BytesIO(image), mimetype=image_b64.mimetype, attachment_filename=filename)


@app.route('/adm/uploadfile', methods=['POST', 'GET'])
def file_uploaded():
    if request.method == 'POST':
        if not request.form.get('password') == os.getenv('PASSWORD'):
            flash("Wrong Password")
            return redirect("/adm/uploadfile")
        # check if the post request has the file part
        if 'files' not in request.files:
            return redirect("/adm/uploadfile")
        files = request.files.getlist('files')
        # if user does not select file, browser also
        # submit an empty part without filename
        for file in files:
            if file.filename == '':
                flash("No files")
                return redirect("/adm/uploadfile")
            data = standard_b64encode(file.read()).decode()
            database_object = ImageBase64(filename=file.filename, mimetype=file.mimetype, data=data)
            db.session.add(database_object)

        db.session.commit()
    return render_template("adm/uploadfile.html")


if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
