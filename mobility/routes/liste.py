from flask import Blueprint, render_template, request, flash, redirect, url_for
from mobility.models.liste import get_airports, get_flight_details, get_flight_details_by_day  

bp = Blueprint('liste', __name__, url_prefix='/liste')


# Route pour afficher les aéroports et les détails des vols
@bp.route('/', methods=['GET', 'POST'])
def afficher_liste_aeroports():
    """
    Affiche la liste des aéroports et, si un aéroport est sélectionné via un formulaire, affiche les détails des vols associés. 
    
    Fonctionnement : 
        - Lorsqu'un utilisateur charge la page pour la première fois avec une méthode GET, la fonction affiche simplement la liste des aéroports. 
        - Lorsqu'un utilisateur soumet le formulaire avec aéroport sélectionné via POST, la fonction récupère l'ID de l'aéroport et affiche : 
            - Les détails des vols pour l'aéroport sélectionné.
            - Les détails des vols regroupés par jour pour l'aéroport sélectionné.
        - Si aucun aéroport n'est sélectionné dans le formulaire, un message d'erreur est affiché demandant à l'utilisateur de choisir un aéroport. 
        
    Input : 
        - Aucun paramètre d'entrée direct, la fonction récupère les données à partir des formulaires POST et des bases de données. 
    
    Output : 
        - str : Le modèle HTML 'liste.html' avec les informations suivantes : 
            - 'aeroport_list' : liste des aéroports récupérée de la base de données. 
            - 'flight_details' : Détails des vols pour l'aéroport sélectionné (si soumis)
            - 'flight_by_day' : Détails des vols par jour pour l'aéroport sélectionné (si soumis)
            - 'selected_airport_id' : L'ID de l'aéroport sélectionné dans le formulaire (si soumis)
    
    """
    aeroport_list = []
    flight_details = []
    flight_by_day = []
    selected_airport_id = None

    # Check if user is on Windows (for select box styling)
    ua_string = request.headers.get("User-Agent", "")
    windows = ("windows nt" in ua_string.lower() or "win64" in ua_string.lower())

    # Get the list of airports with basic error handling
    try:
        aeroport_list = get_airports()
    except Exception as e:
        flash(f"Error retrieving airports: {e}", "error")
        return render_template('liste.html',
                               aeroport_list=[],
                               flight_details=[],
                               flight_by_day=[],
                               selected_airport_id=None,
                               windows=windows)

    if request.method == 'POST':
        if 'reset' in request.form:
            return redirect(url_for('liste.afficher_liste_aeroports'))

        # Otherwise, the "Search" button was clicked
        selected_airport_id = request.form.get('airport_id')
        if not selected_airport_id:
            flash("Veuillez sélectionner un aéroport.", "error")
        else:
            try:
                flight_details = get_flight_details(selected_airport_id)
                flight_by_day = get_flight_details_by_day(selected_airport_id)
            except Exception as e:
                flash(f"Database error: {e}", "error")
                flight_details = []
                flight_by_day = []

    return render_template(
        'liste.html',
        aeroport_list=aeroport_list,
        flight_details=flight_details,
        flight_by_day=flight_by_day,
        selected_airport_id=selected_airport_id,
        windows=windows
    )
