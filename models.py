from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    __table_args__ = (CheckConstraint('age >= 0', name='check_age_positive'),)

    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return name

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")
        return email

    @validates('age')
    def validate_age(self, key, age):
        if age < 0:
            raise ValueError("Age must be 0 or greater")
        return age
