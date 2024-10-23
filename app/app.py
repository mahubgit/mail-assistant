from flask import Flask, render_template, request, redirect, url_for
import os
import imaplib  # Ajoutez ceci pour importer le module imaplib
import email
from email.header import decode_header
from data_preparation import fetch_incoming_emails, fetch_sent_emails
from dashboard import generate_dashboard_data, add_event_to_calendar


app = Flask(__name__)

def test_imap_connection():
    """Teste la connexion au serveur IMAP."""
    try:
        # Connexion au serveur IMAP
        mail = imaplib.IMAP4_SSL(os.getenv('IMAP_SERVER'))
        mail.login(os.getenv('IMAP_USER'), os.getenv('IMAP_PASSWORD'))
        mail.select("inbox")  # Sélectionne la boîte de réception
        mail.logout()  # Se déconnecte
        return "Connexion réussie!"
    except Exception as e:
        return f"Erreur de connexion : {e}"
    
@app.route('/')
def index():
    # Récupération des emails entrants
    incoming_emails = fetch_incoming_emails()
    return render_template('index.html', emails=incoming_emails)

@app.route('/dashboard')
def dashboard():
    # Obtenez les données du tableau de bord
    dashboard_data = generate_dashboard_data()
    return render_template('dashboard.html', data=dashboard_data)

@app.route('/respond/<email_id>', methods=['GET', 'POST'])
def respond(email_id):
    if request.method == 'POST':
        # Récupérer les informations du formulaire
        subject = request.form['subject']
        location = request.form['location']
        date = request.form['date']
        
        # Ajouter l'événement au calendrier
        add_event_to_calendar(subject, location, date)
        return redirect(url_for('dashboard'))
    
    return render_template('email_response.html', email_id=email_id)

@app.route('/test')
def test():
    # Exécute la fonction de récupération des emails entrants
    incoming_emails = fetch_incoming_emails()
    return render_template('test.html', incoming_emails=incoming_emails)

@app.route('/test_imap')
def test_imap():
    result = test_imap_connection()
    return render_template('test_imap.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
