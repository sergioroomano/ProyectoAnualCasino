import uuid

from flask import Blueprint, render_template, request
from casino.database.db import SessionLocal
from casino.database.models import User

o_ppt = Blueprint('o_ppt', __name__, template_folder='templates')

def get_all_usernames():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [user.username for user in users]

def get_all_id():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [user.id for user in users]

def create_user_id():
    return str(uuid.uuid4())

def create_user(username):
    if username not in get_all_usernames():
        db = SessionLocal()
        new_id = User(id=create_user_id())
        db.add(new_id)
        db.commit()
        db.refresh(new_id)
        db.close()

        new_user = User(username=username)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()

        return new_user
    return "User already exists."

@o_ppt.route('/online-ppt', methods=['GET', 'POST'])
def online_ppt():
    
    if request.method == "POST":
        username = request.form['username']
        all_usernames = get_all_usernames()
        all_id = get_all_id()

        print(all_usernames)
        print(all_id)

        create_user(username)

        # Check if the user was saved to the database
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()

        if user is not None:
            print(f"User {username} was saved to the database.")
        else:
            print(f"User {username} was not found in the database.")

    return render_template('online-ppt.html')

@p_ppt.route('/wipe-users', methods=['GET'])
def wipe_users():
    wipe_users()
    return "Users wiped."
