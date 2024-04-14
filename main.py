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

# Funcion que Controla la admision de datos desde la front-end
# Los datos recibidos estan en el formato de [{ficha_nombre_id: [zonas_ocupadas]}]
@app.route('/drop-zone', methods=['POST'])
def handle_drop_zone():
    print("Chip Data Recieved")
    print("Chip Data: ", request.json)
    session["data"] = [request.json]
    print("Created session data with: ", request.json)
    print("Session data: ", session["data"])

    funcionalidad_ruleta()
    return jsonify({"message": "Data received"}), 200

# Función base de la funcionalidad de la ruleta
def funcionalidad_ruleta():
    numero_ganador = random.randint(0,37)
    for entry in session["data"]:
        for ficha in entry:
            print("FICHA: ", ficha)
            ficha_valor = int((ficha.split("-")[1]).split("_")[0])

            ficha_posiciones = []
            for zona in entry[ficha]:
                ficha_posiciones.append(int(zona.split("-")[1]))

            calcular_ganador(ficha_valor, ficha_posiciones, numero_ganador)
            print("FICHA VALOR: ", ficha_valor)
            print("FICHA POSICION: ", ficha_posiciones)

    return

def calcular_ganador(ficha_valor, ficha_posiciones, numero_ganador):
    numeros_rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    numeros_negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    numeros_par =  [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
    numeros_impar = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
    numeros_1_12 = list(range(1,13))
    numeros_13_24 = list(range(13,25))
    numeros_25_37 = list(range(25,37))
    numeros_1_18 = list(range(1,19))
    numeros_19_37 = list(range(19,37))
    numeros_2_1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
    numeros_2_2 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
    numeros_2_3 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

    posibles_apuestas = {
    "rojo": (numeros_rojos, 1),
    "negro": (numeros_negros, 1),
    "par": (numeros_par, 1),
    "impar": (numeros_impar, 1),
    "1_12": (numeros_1_12, 2),
    "13_24": (numeros_13_24, 2),
    "25_37": (numeros_25_37, 2),
    "1_18": (numeros_1_18, 1),
    "19_37": (numeros_19_37, 1),
    "2_1": (numeros_2_1, 2),
    "2_2": (numeros_2_2, 2),
    "2_3": (numeros_2_3, 2)
    }

    propiedades_numero_ganador = []

    print("NUMERO GANADOR: ", numero_ganador)
    for apuesta in posibles_apuestas:
        if numero_ganador in posibles_apuestas[apuesta][0]:
            propiedades_numero_ganador.append(apuesta)
    print("Propiedades de numero ganador: ", propiedades_numero_ganador)

    # Calculod de tasa de pago
    diccionario_multiplicadores = {1: 35, 2: 17, 3: 11, 4: 8, 6: 5}

    if len(ficha_posiciones) == 1 and not ficha_posiciones[0].isdigit():
        if ficha_posiciones[0] in propiedades_numero_ganador:
            print("Has ganado!")
            print("Has ganado: ", ficha_valor * posibles_apuestas[ficha_posiciones[0]][1])
        else:
            print("Has perdido!")
    print("DEBUG FOR: ", numero_ganador, "in", ficha_posiciones)
    if numero_ganador in ficha_posiciones:
        multiplicador = diccionario_multiplicadores[len(ficha_posiciones)]
        print("Has ganado!")
        print("Has ganado: ", ficha_valor * multiplicador)

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
