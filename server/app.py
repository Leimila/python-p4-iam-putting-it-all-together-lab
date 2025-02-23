# # #!/usr/bin/env python3

# # from flask import request, session
# # from flask_restful import Resource
# # from sqlalchemy.exc import IntegrityError

# # from config import app, db, api
# # from models import User, Recipe

# # class Signup(Resource):
# #     pass

# # class CheckSession(Resource):
# #     pass

# # class Login(Resource):
# #     pass

# # class Logout(Resource):
# #     pass

# # class RecipeIndex(Resource):
# #     pass

# # api.add_resource(Signup, '/signup', endpoint='signup')
# # api.add_resource(CheckSession, '/check_session', endpoint='check_session')
# # api.add_resource(Login, '/login', endpoint='login')
# # api.add_resource(Logout, '/logout', endpoint='logout')
# # api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


# # if __name__ == '__main__':
# #     app.run(port=5555, debug=True)
# #!/usr/bin/env python3

# from flask import Flask, request, session, jsonify
# from flask_restful import Resource, Api
# from flask_migrate import Migrate
# from sqlalchemy.exc import IntegrityError

# # from config import app, db
# from config import app, db

# # from models import User, Recipe
# from server.models import User, Recipe


# # Initialize Flask-Migrate
# migrate = Migrate(app, db)

# # Initialize API
# api = Api(app)

# # ------------------- AUTHENTICATION ROUTES ------------------- #

# class Signup(Resource):
#     def post(self):
#         data = request.get_json()
#         try:
#             new_user = User(
#                 username=data["username"],
#                 email=data["email"],
#                 password_hash=data["password"]  # Ensure User model hashes passwords
#             )
#             db.session.add(new_user)
#             db.session.commit()
#             session["user_id"] = new_user.id  # Log in the user automatically

#             return jsonify({"message": "User created successfully!", "user": new_user.to_dict()})
        
#         except IntegrityError:
#             db.session.rollback()
#             return {"error": "Username or email already exists"}, 400

# class CheckSession(Resource):
#     def get(self):
#         user_id = session.get("user_id")
#         if user_id:
#             user = User.query.get(user_id)
#             return user.to_dict(), 200
#         return {"error": "Unauthorized"}, 401

# class Login(Resource):
#     def post(self):
#         data = request.get_json()
#         user = User.query.filter_by(username=data["username"]).first()

#         if user and user.authenticate(data["password"]):  # Ensure User model has an authenticate method
#             session["user_id"] = user.id
#             return user.to_dict(), 200
#         return {"error": "Invalid credentials"}, 401

# class Logout(Resource):
#     def delete(self):
#         session.pop("user_id", None)
#         return {"message": "Logged out successfully"}, 200

# # ------------------- RECIPE ROUTES ------------------- #

# class RecipeIndex(Resource):
#     def get(self):
#         recipes = Recipe.query.all()
#         return [recipe.to_dict() for recipe in recipes], 200

#     def post(self):
#         data = request.get_json()
#         new_recipe = Recipe(
#             title=data["title"],
#             ingredients=data["ingredients"],
#             instructions=data["instructions"],
#             user_id=session.get("user_id")  # Ensure user is logged in
#         )

#         db.session.add(new_recipe)
#         db.session.commit()
#         return new_recipe.to_dict(), 201

# # ------------------- REGISTER API RESOURCES ------------------- #

# api.add_resource(Signup, "/signup", endpoint="signup")
# api.add_resource(CheckSession, "/check_session", endpoint="check_session")
# api.add_resource(Login, "/login", endpoint="login")
# api.add_resource(Logout, "/logout", endpoint="logout")
# api.add_resource(RecipeIndex, "/recipes", endpoint="recipes")

# # ------------------- MAIN APP RUNNER ------------------- #

# if __name__ == "__main__":
#     app.run(port=5555, debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import db  # Ensure config.py contains db = SQLAlchemy()
from models import User, Recipe  # Ensure models.py defines these classes

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Define a simple route to check if the server is running
@app.route('/')
def home():
    return "Flask app is running!"

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
