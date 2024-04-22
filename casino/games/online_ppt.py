import uuid
import shortuuid

from flask import Blueprint, render_template, request, session
from flask_socketio import join_room, send, leave_room

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

def room_exists(room_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM rooms WHERE room_id = %s"
        cursor.execute(sql, (room_id,))
        result = cursor.fetchone()
    connection.close()

    return result is not None

def insert_user(username, user_id):
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

def insert_room(room_id, user_id):
    connection = get_db_connection()
    if not room_exists(room_id):
        join_room(room_id)
        send(user_id + ' has entered the room.', room=room_id)
        with connection.cursor() as cursor:
            sql = "INSERT INTO rooms (room_id, player_1) VALUES (%s, %s)"
            cursor.execute(sql,(room_id,user_id))
        connection.commit()
        connection.close()
    else:
        create_room()

    return render_template('online-ppt-session.html', ROOM_ID = room_id)

@o_ppt.route('/online-ppt', methods=['GET', 'POST'])
def online_ppt():

    if request.method == "POST":
        username = request.form['username']
        user_id = uuid.uuid4()
        session['user_id'] = user_id

        print(username)

        return insert_user(username, user_id)

    return render_template('online-ppt.html')

@o_ppt.route('/wipe-users')
def clear_users_table():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE users")
    connection.commit()
    connection.close()
    return "Users wiped."

@o_ppt.route('/wipe-rooms')
def clear_rooms_table():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE rooms")
    connection.commit()
    connection.close()
    return "Rooms wiped."

@o_ppt.route('/create-room')
def create_room():
    user_id = session.get('user_id')
    room_id_gen = shortuuid.ShortUUID("23456789ABCDEF")
    room_id = room_id_gen.random(4)
    insert_room(room_id, user_id)

    return render_template('online-ppt-session.html', ROOM_ID = room_id)







