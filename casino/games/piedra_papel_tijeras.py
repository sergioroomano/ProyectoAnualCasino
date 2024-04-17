from flask import Blueprint, render_template, request
import random

ppt = Blueprint('ppt', __name__, template_folder='templates')

@ppt.route('/piedra-papel-tijera', methods=['GET', 'POST'])
def rock_paper_scissors():
    if request.method == 'POST':
        user_choice = request.form['choice']
        server_choice = random.choice(['piedra', 'papel', 'tijera'])
        result = determinar_ganador(user_choice, server_choice)
        return render_template('piedra_papel_tijera.html', user_choice=user_choice, server_choice=server_choice, result=result)
    return render_template('piedra_papel_tijera.html', user_choice=None, server_choice=None, result=None)

def determinar_ganador(user, server):
    if user == server:
        return 'Empate!'
    elif (user == 'piedra' and server == 'tijera') or \
         (user == 'tijera' and server == 'papel') or \
         (user == 'papel' and server == 'piedra'):
        return 'Has Ganado!'
    else:
        return 'Has Perdido!'
