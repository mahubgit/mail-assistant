# Utiliser l'image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Installer le modèle de langue français pour spaCy
RUN python -m spacy download fr_core_news_md

# Copier le reste des fichiers de l'application
COPY . .

# Exposer le port que l'application utilise
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "app/app.py"]