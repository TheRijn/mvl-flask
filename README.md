# Portfolio Website

A quick portfolio website made to run on Heroku without any storage bucket.


Tables can be created with:
```python
    >>> from app import db
    >>> db.create_all()
```

## Missing features

- Migrations
- Multiple categories
- An admin interface to add things (other then pictures) to the portfolio.
- A login-system
- A JQuery-free website