import json
import re
import joblib
import pymysql
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split



with open("french_stopwords.json", "r", encoding="utf-8") as file:
    stopwords_data = json.load(file)
french_stopwords = stopwords_data["french_stopwords"]


def clean_text(text):
    text = text.lower() # Mettre en minuscule
    text = re.sub(r'[^\w\s]', '', text) # Supprimer les caractères spéciaux
    return text

# Connect to MySQL
def get_db_connection():
    return pymysql.connect(host="localhost", user="flask_user", password="password", database="flask_db")

def retrain_model():
    print(" Retraining model...")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tweets")
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()

    if not data:
        print("❌ No new data found for retraining.")
        return

    response = {
        "label": [row[0] for row in data],
        "text": [row[1] for row in data]
    }
    df = pd.DataFrame(response, columns=["text", "label"])

    df["text_clean"] = df["text"].apply(clean_text)

    vectorizer = CountVectorizer(stop_words=french_stopwords, max_features=100)
    X = vectorizer.fit_transform(df["text_clean"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Save updated model & vectorizer
    joblib.dump(model, "logistic_regression_model.joblib")
    joblib.dump(vectorizer, "vectorizer.joblib")

    print("✅ Model retrained successfully!")

if __name__ == "__main__":
    retrain_model()