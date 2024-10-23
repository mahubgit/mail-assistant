import os
import pandas as pd
from sklearn.model_selection import train_test_split
import imaplib
import email
from email.header import decode_header

# Chemin des données d'entrée
DATA_DIR = 'data/'
RAW_DATA_FILE = os.path.join(DATA_DIR, 'raw_data.csv')  # Fichier de données brutes
TRAIN_DATA_FILE = os.path.join(DATA_DIR, 'train_data.csv')  # Fichier de données d'entraînement
VALIDATION_DATA_FILE = os.path.join(DATA_DIR, 'validation_data.csv')  # Fichier de données de validation

def load_data():
    """Charge les données brutes à partir d'un fichier CSV."""
    try:
        data = pd.read_csv(RAW_DATA_FILE)
        print(f"Données chargées avec succès depuis {RAW_DATA_FILE}.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        return None

def deduplicate_data(data):
    """Supprime les doublons dans le DataFrame."""
    original_size = len(data)
    data = data.drop_duplicates()
    new_size = len(data)
    print(f"{original_size - new_size} doublons supprimés.")
    return data

def split_data(data):
    """Divise les données en ensembles d'entraînement et de validation."""
    train_data, validation_data = train_test_split(data, test_size=0.2, random_state=42)
    return train_data, validation_data

def save_data(train_data, validation_data):
    """Sauvegarde les ensembles de données d'entraînement et de validation."""
    train_data.to_csv(TRAIN_DATA_FILE, index=False)
    validation_data.to_csv(VALIDATION_DATA_FILE, index=False)
    print(f"Données d'entraînement et de validation sauvegardées dans {TRAIN_DATA_FILE} et {VALIDATION_DATA_FILE}.")

def prepare_data():
    """Prépare les données pour l'entraînement."""
    raw_data = load_data()
    if raw_data is not None:
        cleaned_data = deduplicate_data(raw_data)
        train_data, validation_data = split_data(cleaned_data)
        save_data(train_data, validation_data)
    else:
        print("La préparation des données a échoué en raison de problèmes de chargement.")

def fetch_incoming_emails():
    """Récupère les emails entrants depuis un serveur IMAP."""
    IMAP_SERVER = os.getenv('IMAP_SERVER')
    IMAP_USER = os.getenv('IMAP_USER')
    IMAP_PASSWORD = os.getenv('IMAP_PASSWORD')

    try:
        # Connexion au serveur IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(IMAP_USER, IMAP_PASSWORD)
        mail.select("inbox")  # Sélectionner la boîte de réception

        # Récupérer les IDs des emails
        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()

        emails = []
        for email_id in email_ids:
            # Récupérer chaque email
            res, msg = mail.fetch(email_id, '(RFC822)')
            raw_email = msg[0][1]
            msg = email.message_from_bytes(raw_email)

            # Décoder le sujet
            subject, _ = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            emails.append(subject)  # Ajoutez le sujet à la liste des emails

        mail.logout()  # Déconnexion
        return emails
    except Exception as e:
        print(f"Erreur lors de la récupération des emails : {e}")
        return []
    
def fetch_sent_emails():
    """Récupère les emails envoyés depuis la boîte "Sent"."""
    try:
        mail = imaplib.IMAP4_SSL(os.getenv('IMAP_SERVER'))
        mail.login(os.getenv('IMAP_USER'), os.getenv('IMAP_PASSWORD'))
        mail.select("Sent")  # Sélectionne la boîte des emails envoyés
        
        status, messages = mail.search(None, 'ALL')  # Récupère tous les messages
        email_ids = messages[0].split()

        sent_emails = []
        for email_id in email_ids:
            res, msg = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg[0][1])
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            # Ajoutez d'autres informations nécessaires
            sent_emails.append({
                'id': email_id,
                'subject': subject,
                'from': msg['From'],
                'date': msg['Date'],
                # Ajoutez d'autres champs si nécessaire
            })

        mail.logout()
        return sent_emails

    except Exception as e:
        print(f"Erreur lors de la récupération des emails envoyés : {e}")
        return []


if __name__ == "__main__":
    prepare_data()
