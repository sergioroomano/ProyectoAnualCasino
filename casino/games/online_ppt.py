import uuid

from flask import Blueprint, render_template, request

from casino.database.db import get_db_connection

o_ppt = Blueprint('o_ppt', __name__, template_folder='templates')

def user_exists(username):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
    connection.close()

    return result is not None

def insert_user(username):
    user_id = uuid.uuid4()

    connection = get_db_connection()
    if not user_exists(username):
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (id, username) VALUES (%s, %s)"
            cursor.execute(sql, (user_id, username))
        connection.commit()
        connection.close()
    else:
        return "Username taken"

    return render_template('online-ppt-create-session.html', USER_ID = user_id, USERNAME = username)

@o_ppt.route('/online-ppt', methods=['GET', 'POST'])
def online_ppt():

    if request.method == "POST":
        username = request.form['username']

        print(username)

        return insert_user(username)

    return render_template('online-ppt.html')

@o_ppt.route('/wipe-users')
def clear_users_table():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE users")
    connection.commit()
    connection.close()
    return "Users wiped."
