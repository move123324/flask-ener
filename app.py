from flask import Flask
from mobility.db import init_app
from mobility.routes.liste import bp as liste_bp

def create_app():
    app = Flask(__name__)
    # Path for local SQLite DB
    app.config["DATABASE"] = "instance/db.sqlite"
    # For flash messages
    app.config["SECRET_KEY"] = "dev"

    # Initialize DB (register teardown, CLI commands, etc.)
    init_app(app)

    # Register your blueprint
    app.register_blueprint(liste_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
