# Algorithme Avancée:
## How to Setup 

### Lancer l'installation des dépendances
```
pip install -r requirements.txt
```

### Initialiser la base de donnée
```
python setupDb.py
```

### Lancer l'application Flask
```
flask run
```

# Appel des Endpoints

## POST : predict
http://127.0.0.1:5000/predict

Cet endpoint permet de soumettre des tweets pour qu'ils soient évalués.
Le Body accepte un format JSON tel que :
```
[   
    "Tu es un idiot.",
    "Je deteste ça.",
    "Une très bonne vidéo, claire et précise, bravo.",
    "je suis content.",
    "bonjour"
]
```

## GET : tweets
http://127.0.0.1:5000/tweets

Cet endpoint permet de récupérer tous les tweets qui ont été évalués.

## Automatisation du réapprentissage sur Windows
```
python schedulTrain.py
```

## Réapprentissage manuel
```
python retrain.py
```


