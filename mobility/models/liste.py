from mobility.db import get_db

def get_airports():
    """
    Récupère la liste des aéroports ayant un nom défini. 
    
    Input : 
        - Aucun 
    
    Fonctionnement : 
        - Se connecte à la base de données via 'get_db()'
        - Exécute une requête SQL pour récupérer les codes IATA et les noms des aéroports 
        - Filtre les résultats pour exclure les aéroports sans nom 
        - Trie les résultats par ordre alphabétique des noms
        
    Output : 
        - Retourne une liste de tuples contenant (iata_code, name)
    """
    db = get_db()
    return db.execute("SELECT iata_code, name FROM airport WHERE name is NOT NULL ORDER BY name ASC").fetchall()


def get_flight_details(airport_id):
    """
    Récupère le nombre de vols par type d'avion pour un aéroport donne. 
    
    Input : 
        - airport_id (str) : code IATA de l'aéroport de départ
        
    Fonctionnement : 
        - Se connecte à la base de données via 'get_db()'
        - Exécute une requête SQL pour récupérer les types d'avions ayant décollé de l'aéroport
        - Compte le nombre de vols pour chaque type d'avion 
        - Regroupe les résultats par type d'avion 
    
    Output : 
        - Retourne une liste de tuples contenant (aircraft_type, total_vols)
    """
    db = get_db()
    return db.execute("""
        SELECT ac.aircraft_type AS aircraft_type, 
               COUNT(*) AS total_vols
        FROM flight f
        JOIN aircraft ac ON f.iata_aircraft = ac.iata_aircraft
        WHERE f.iata_departure = ?
        GROUP BY ac.aircraft_type
    """, (airport_id,)).fetchall()

def get_flight_details_by_day(airport_id):
    """
    Récupère le nombre de vols par jour de la semaine pour un aéroport donné.
    
    Input : 
        - airport_id (str) : code IATA de l'aéroport de départ 
        
    Fonctionnement : 
        - Se connecte à la base de données via 'get_db()'
        - Exécute une requête SQL pour compter les vols ayant décollé de l'aéroport pour chaque jour de la semaine 
        - Utilise 'strftime('%w', flight_date)' pour obtenir le jour (0 = dimanche, ..., 6 = samedi)
        - Regroupe les résultats par jour de la semaine 
        
    Output : 
        - Retourne une liste de tuples contenant (day_of_week, total_vols)
    """
    db = get_db()
    return db.execute("""
        SELECT
            CASE strftime('%w', f.flight_date)
                WHEN '1' THEN 'Monday'
                WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday'
                WHEN '4' THEN 'Thursday'
                WHEN '5' THEN 'Friday'
                WHEN '6' THEN 'Saturday'
                WHEN '0' THEN 'Sunday'
            END AS day_of_week,
            COUNT(*) AS total_vols
        FROM flight f
        WHERE f.iata_departure = ?
        GROUP BY day_of_week
        ORDER BY
            CASE strftime('%w', f.flight_date)
                WHEN '1' THEN 1  -- Monday
                WHEN '2' THEN 2  -- Tuesday
                WHEN '3' THEN 3  -- Wednesday
                WHEN '4' THEN 4  -- Thursday
                WHEN '5' THEN 5  -- Friday
                WHEN '6' THEN 6  -- Saturday
                WHEN '0' THEN 7  -- Sunday
            END
    """, (airport_id,)).fetchall()