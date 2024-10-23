import imaplib
import os

IMAP_SERVER = os.getenv('IMAP_SERVER')
IMAP_USER = os.getenv('IMAP_USER')
IMAP_PASSWORD = os.getenv('IMAP_PASSWORD')

try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(IMAP_USER, IMAP_PASSWORD)
    mail.select("inbox")
    print("Connexion réussie!")
    mail.logout()
except Exception as e:
    print(f"Erreur de connexion : {e}")
