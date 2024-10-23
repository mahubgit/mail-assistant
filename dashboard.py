import os

def generate_dashboard_data():
    """Génère les données nécessaires pour le tableau de bord."""
    # Ici, vous pouvez ajouter votre logique pour récupérer et préparer les données
    # Pour l'instant, on renvoie une liste fictive
    return [
        {'email_id': 1, 'subject': 'Proposition de réunion', 'sender': 'example1@example.com'},
        {'email_id': 2, 'subject': 'Rapport à soumettre', 'sender': 'example2@example.com'},
    ]

def add_event_to_calendar(subject, location, date):
    """Ajoute un événement au calendrier."""
    # Implémentez ici la logique pour ajouter un événement à votre calendrier
    print(f"Événement ajouté : {subject} à {location} le {date}")
