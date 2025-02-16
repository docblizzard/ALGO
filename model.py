import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import json

with open("dataset.json", "r", encoding="utf-8") as file:
    dateset_data = json.load(file)

with open("french_stopwords.json", "r", encoding="utf-8") as file:
    stopwords_data = json.load(file)

french_stopwords = stopwords_data["french_stopwords"]

dataset = [{"text": dateset_data["text"][i], "label": dateset_data["label"][i]} for i in range(len(dateset_data["text"]))]


def clean_text(text):
    text = text.lower() # Mettre en minuscule
    text = re.sub(r'[^\w\s]', '', text) # Supprimer les caractères spéciaux
    return text

# Conversion en DataFrame
df = pd.DataFrame(dataset)
df['text_clean'] = df['text'].apply(clean_text)

# Vectorisation (bag of words)
vectorizer = CountVectorizer(stop_words=french_stopwords, max_features=100)
X = vectorizer.fit_transform(df['text_clean'])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)
print("Modèle entraîné avec succès.")

print("Vectorisation terminée.")
print(df)

# Prédictions
y_pred = model.predict(X_test)
# Rapport de classification
print("Rapport de classification :")
print(classification_report(y_test, y_pred))
# Matrice de confusion
print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))
joblib.dump(model, 'logistic_regression_model.joblib')

new_comments = [
    "Je ne supporte pas cette personne.",
    "Cette vidéo est incroyable, merci pour votre travail.",
    "Arrête de dire n'importe quoi, imbécile.",
    "Une excellente présentation, bravo à toute l'équipe.",
    "Tu es un idiot.",
    "Pourquoi es-tu aussi stupide?"
]

def predictNew(new_comments):
    print("Modèle enregistré avec succès.")

    loaded_model = joblib.load('logistic_regression_model.joblib')

    # Prétraitement des nouveaux commentaires
    new_comments_clean = [clean_text(comment) for comment in new_comments]
    new_comments_vectorized = vectorizer.transform(new_comments_clean)

    # Utiliser le modèle chargé pour obtenir les probabilités
    probabilities = loaded_model.predict_proba(new_comments_vectorized)
    predictions = loaded_model.predict(new_comments_vectorized)

    # Map the probabilities to sentiment scores (-1 to 1)
    response = {}
    for comment, label in zip(new_comments, predictions.tolist()):  # Convert to list
        score = label  # Assuming label is already in the desired range (-1 to 1)
        response[comment] = score
    # response = {comment: 1 if label == 0 else -1 for comment, label in zip(new_comments, predictions)}
    
    for comment, label in zip(new_comments, predictions):
        print(f"Commentaire : '{comment}' -> {label}")
    return response
predictNew(new_comments)