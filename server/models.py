# from sqlalchemy.orm import validates
# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy_serializer import SerializerMixin

# from config import db, bcrypt

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)  # Primary key
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     _password_hash = db.Column(db.String(128), nullable=False)  # Private password hash field

#     bio = db.Column(db.Text)  # Added bio field
#     image_url = db.Column(db.String)  # Added image_url field

#     # Serialize only necessary fields
#     serialize_rules = ('-recipes.user',)

#     @hybrid_property
#     def password_hash(self):
#         return self._password_hash

#     @password_hash.setter
#     def password_hash(self, password):
#         self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

#     def authenticate(self, password):
#         return bcrypt.check_password_hash(self._password_hash, password)

#     def __repr__(self):
#         return f"<User {self.username}>"

# class Recipe(db.Model, SerializerMixin):
#     __tablename__ = 'recipes'
    
#     id = db.Column(db.Integer, primary_key=True)  # Primary key
#     title = db.Column(db.String(255), nullable=False)
#     instructions = db.Column(db.Text, nullable=False)
#     minutes_to_complete = db.Column(db.Integer, nullable=False)  # Added minutes_to_complete field
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key linking to User

#     user = db.relationship('User', backref='recipes')

#     def __repr__(self):
#         return f"<Recipe {self.title}>"
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    bio = db.Column(db.String, nullable=True)

    recipes = db.relationship("Recipe", backref="user", lazy=True)

    def __init__(self, username, password, image_url=None, bio=None):
        self.username = username
        self.password_hash = password  # Uses the setter to hash the password
        self.image_url = image_url
        self.bio = bio

    @property
    def password_hash(self):
        raise AttributeError("Password hash is not readable")

    @password_hash.setter
    def password_hash(self, password):
        """Hashes password before storing it in the database"""
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        """Checks if provided password matches the hashed password"""
        return bcrypt.check_password_hash(self._password_hash, password)

    @validates("username")
    def validate_username(self, key, username):
        """Ensures username is not empty and unique"""
        if not username:
            raise ValueError("Username cannot be empty")
        return username

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates("title")
    def validate_title(self, key, title):
        """Ensures the recipe has a title"""
        if not title:
            raise ValueError("Title cannot be empty")
        return title

    @validates("instructions")
    def validate_instructions(self, key, instructions):
        """Ensures instructions are at least 50 characters long"""
        if not instructions or len(instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long")
        return instructions
