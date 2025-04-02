from flask import Flask
from mobility.db import init_app
from mobility.routes.liste import bp as liste_bp

def create_app():
    app = Flask(__name__)

    app.config["DATABASE"] = "instance/db.sqlite"

    app.config["SECRET_KEY"] = "dev"


    init_app(app)


    app.register_blueprint(liste_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
