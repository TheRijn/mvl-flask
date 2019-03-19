from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    @staticmethod
    def get_posts():
        return Post.query.order_by(Post.priority).all()

    @staticmethod
    def get_posts_with_category(category_id):
        return Post.query.filter(Post.category_id == category_id).order_by(Post.priority).all()


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(80), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
