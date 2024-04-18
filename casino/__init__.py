from flask import Flask, render_template, request
from .games.roullete import ruleta_bp
from .games.piedra_papel_tijeras import ppt

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    app.register_blueprint(ruleta_bp)
    app.register_blueprint(ppt)

    @app.route('/')
    def principal():
        return render_template('principal.html')

    @app.route('/juegos')
    def select_juego():
        return render_template('juegos.html')
    
    @app.route('/online-ppt', methods=['GET', 'POST'])
    def online_ppt():
        username = request.form['username']
        print(username)
        return render_template('ppt.html')
    return app