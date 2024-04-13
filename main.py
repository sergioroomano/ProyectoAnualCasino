from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def principal():
    return render_template('principal.html')

@app.route('/juegos')
def select_juego():
    return render_template('juegos.html')

# Ruleta
@app.route('/ruleta')
def ruleta():
    return render_template('ruleta.html',resultado=None)

# Funcion Archaica de lo que seria girar la ruleta CAMBIAR
@app.route('/drop-zone', methods=['POST'])
def handle_drop_zone():
    print("Chip Data Recieved")
    print("Chip Data: ", request.json)
    session["data"] = [request.json]
    print("Created session data with: ", request.json)
    print("Session data: ", session["data"])
    return jsonify({"message": "Data received"}), 200

@app.route('/girar-ruleta', methods=['POST'])
def girar_ruleta():
    pass

def funcionalidad_ruleta(data):
    numero_ganador = random.randint(0,37)

    dinero_apostado = 0

    numeros_zona_apostados = []
    numeros_apostados = set()

    for apuesta in data:
        dinero_apostado += int((apuesta["ficha"].split("-"))[1])
        numeros_zona_apostados += apuesta["zone"]

    for zona in numeros_zona_apostados:
        numeros_apostados.add((zona.split("-")[1]))

    print(dinero_apostado)
    print(numeros_apostados)


# Piedra Papel o Tijera contra el servidor
@app.route('/piedra-papel-tijera', methods=['GET', 'POST'])
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
