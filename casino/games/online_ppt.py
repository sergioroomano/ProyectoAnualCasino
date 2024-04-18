import uuid

from flask import Blueprint, render_template, request

o_ppt = Blueprint('o_ppt', __name__, template_folder='templates')

def inser_user(username):
    user_id = uuid.uuid4()

    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO users (id, username) VALUES (%s, %s)"
        cursor.execute(sql, (user_id, username))
    connection.commit()
    connection.close()

    return user_id

@o_ppt.route('/online-ppt', methods=['GET', 'POST'])
def online_ppt():

    if request.method == "POST":
        username = request.form['username']
        insert_user(username)
        print(username)

    return render_template('online-ppt.html')

@o_ppt.route('/wipe-users', methods=['GET'])
def wipe_users():
    return "Users wiped."
