from flask import Flask, render_template
from .games.roullete import ruleta_bp
from .games.piedra_papel_tijeras import ppt
from .games.online_ppt import o_ppt

from casino.database.db import Base, engine
from casino.database.models import User

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    app.register_blueprint(ruleta_bp)
    app.register_blueprint(ppt)
    app.register_blueprint(o_ppt)

    @app.route('/')
    def principal():
        return render_template('principal.html')

    @app.route('/juegos')
    def select_juego():
        return render_template('juegos.html')

    return app