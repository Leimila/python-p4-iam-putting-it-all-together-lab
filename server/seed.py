# from random import randint, choice as rc
# from faker import Faker

# from app import app
# from models import db, Recipe, User

# fake = Faker()

# def seed_database():
#     with app.app_context():
#         print("🔄 Deleting all records...")
#         db.session.query(Recipe).delete()
#         db.session.query(User).delete()
#         db.session.commit()  # Ensure data is wiped before inserting new records

#         print("👤 Creating users...")
#         users = []
#         for _ in range(20):
#             user = User(
#                 username=fake.unique.first_name(),
#                 email=fake.unique.email(),
#                 bio=fake.paragraph(nb_sentences=3),
#                 image_url=fake.image_url()
#             )
#             user.password_hash = user.username + 'password'  # Setting hashed password
#             users.append(user)

#         db.session.add_all(users)
#         db.session.commit()  # Commit users first to get their IDs

#         print("🍽 Creating recipes...")
#         recipes = []
#         for _ in range(100):
#             recipe = Recipe(
#                 title=fake.sentence(),
#                 instructions=fake.paragraph(nb_sentences=8),
#                 minutes_to_complete=randint(15, 90),  # Random time between 15 and 90 minutes
#                 user_id=rc(users).id  # Assign random user
#             )
#             recipes.append(recipe)

#         db.session.add_all(recipes)
#         db.session.commit()

#         print("✅ Seeding complete!")

# if __name__ == "__main__":
#     seed_database()
from random import randint, choice as rc
from faker import Faker
from flask_bcrypt import Bcrypt

from config import app, db
from models import User, Recipe

fake = Faker()
bcrypt = Bcrypt(app)

def seed_database():
    with app.app_context():
        print("🔄 Deleting all records...")
        db.session.query(Recipe).delete()
        db.session.query(User).delete()
        db.session.commit()  # Ensure data is wiped before inserting new records

        print("👤 Creating users...")
        users = []
        for _ in range(20):
            username = fake.unique.first_name()
            email = fake.unique.email()

            user = User(
                username=username,
                email=email,
                bio=fake.paragraph(nb_sentences=3),
                image_url="https://via.placeholder.com/150"  # Using a placeholder image
            )
            user.password_hash = bcrypt.generate_password_hash("password123").decode("utf-8")  # Proper password hashing
            users.append(user)

        db.session.add_all(users)
        db.session.commit()  # Commit users first to get their IDs

        print("🍽 Creating recipes...")
        recipes = []
        for _ in range(100):
            recipe = Recipe(
                title=fake.sentence(),
                instructions=fake.paragraph(nb_sentences=8),
                minutes_to_complete=randint(15, 90),  # Random time between 15 and 90 minutes
                user_id=rc(users).id  # Assign random user
            )
            recipes.append(recipe)

        db.session.add_all(recipes)
        db.session.commit()

        print("✅ Seeding complete!")

if __name__ == "__main__":
    seed_database()
