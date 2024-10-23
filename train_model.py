import os
import torch
from transformers import CamembertTokenizer, CamembertForSequenceClassification
from datasets import load_dataset

# Chemin des données d'entraînement
DATA_DIR = 'app/data/'
TRAIN_DATA_FILE = os.path.join(DATA_DIR, 'train_data.csv')
VALIDATION_DATA_FILE = os.path.join(DATA_DIR, 'validation_data.csv')

# Chargement du modèle pré-entraîné
tokenizer = CamembertTokenizer.from_pretrained('camembert-base')
model = CamembertForSequenceClassification.from_pretrained('camembert-base', num_labels=2)  # Adaptez le nombre de labels

def load_data():
    """Charge les données d'entraînement et de validation."""
    train_data = load_dataset('csv', data_files=TRAIN_DATA_FILE)
    validation_data = load_dataset('csv', data_files=VALIDATION_DATA_FILE)
    return train_data['train'], validation_data['train']

def train_model():
    """Fonction d'entraînement du modèle."""
    train_dataset, validation_dataset = load_data()
    
    # Préparation de l'entraînement
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=16, shuffle=True)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    model.train()
    for epoch in range(3):  # Ajustez le nombre d'époques
        for batch in train_loader:
            optimizer.zero_grad()
            inputs = tokenizer(batch['text'], padding=True, truncation=True, return_tensors='pt')
            labels = batch['label']
            outputs = model(**inputs, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            print(f"Époque {epoch}, Perte : {loss.item()}")

    # Sauvegarder le modèle entraîné
    model.save_pretrained(os.path.join('app/models', 'model'))

if __name__ == "__main__":
    train_model()