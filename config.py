import os

# Configuration des variables d'environnement
IMAP_SERVER = os.getenv('IMAP_SERVER')
IMAP_LOGIN = os.getenv('IMAP_LOGIN')
IMAP_PASSWORD = os.getenv('IMAP_PASSWORD')
MODEL_NAME = os.getenv('MODEL_NAME', 'camembert-base')