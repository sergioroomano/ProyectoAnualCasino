from flask import Blueprint, render_template, request

o_ppt = Blueprint('o_ppt', __name__, template_folder='templates')

@o_ppt.route('/online-ppt', methods=['GET', 'POST'])
def online_ppt():
    if request.method == "POST":
        username = request.form['username']
        print(username)

    return render_template('online-ppt.html')