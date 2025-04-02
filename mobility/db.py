import click
import sqlite3
from flask import current_app, g

def get_db():
    """
    Retourne la connexion à la base de données. Crée la connexion si elle n'existe pas. 
    
    Fonctionnement : 
        - Vérifie si une connexion à la base de données existe dans l'objet global 'g'
        - Si la connexion n'existe pas, une nouvelle connexion est établie en utilisant le chemin de la base de données configurée dans 'current_app.config['DATABASE']
        - La connexion utilise le format de données 'sqlite3.Row', ce qui permet de récupérer les résultats des requêtes sous forme de dictionnaires (au lieu de tuples)
        
    Output : 
        - sqlite3.Connection : la connexion à la base de données
    """

    # g is the shorthand for "globals" and allows registering available in the whole Flask app
    if 'db' not in g:
        # If it's not there, let's create the db connection
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    Ferme la connexion à la base de données si elle existe. 
    
    Input : 
        - e (optionnel) : Aucun usage dans cette fonction. Cela permet de respecter l'interface de Flask pour les gestionnaires de contexte.
        
    Fonctionnement : 
        - Récupère la connexion à la base de données depuis l'objet global 'g'
        - Si la connexoin existe, elle est fermée. 
    
    Output : 
        - None 
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """
    Initialisation de la base de données. 
    
    Fonctionnement : 
        - Cette fonction est appelée pour initialiser la base de données
        - Elle peut être étendue pour ajouter des tables ou des données initiales. 
    
    Output : 
        - None 
    """
    pass

@click.command('init-db')
def init_db_command():
    """
    Commande CLI pour initialiser la base de données. 
    
    Fonctionnement : 
        - Cette fonction est utilisée par Flask pour ajouter une commande CLI 'init-db', qui appelle la fonction 'init-db()'
    
    Output : 
        - None 
    """
    init_db()

def init_app(app):
    """
    Initialise l'application Flask avec des fonctions liées à la base de données. 
    
    Input : 
        - app (Flask) : L'instance de l'application Flask à initialiser. 
    
    Fonctionnement : 
        - Enregistre la fonction 'close_db' pour être exécutée à la fin de chaque requête via 'app.teardown_appcontext()
        - Ajoute la commande CLI 'init-db' à l'application via 'app.cli.add_command()'
    
    Output : 
        - None 
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)