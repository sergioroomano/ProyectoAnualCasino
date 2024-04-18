from flask import Blueprint, render_template, request
from casino.database.db import SessionLocal
from casino.database.models import User

o_ppt = Blueprint('o_ppt', __name__, template_folder='templates')

def create_user(username):
    db = SessionLocal()
    new_user = User(username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user

@o_ppt.route('/online-ppt', methods=['GET', 'POST'])
def online_ppt():
    if request.method == "POST":
        username = request.form['username']
        print(username)

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