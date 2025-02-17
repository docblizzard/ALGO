from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
from model import predictNew
from setupDb import setupDB

app = Flask(__name__)
@app.before_request
def initialize():
    print("hello")
    setupDB()

mysql = MySQL()
mysql.init_app(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'flask_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'flask_db'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json 
    if not isinstance(data, list):
        return jsonify({"error": "Invalid input, expected a list of tweets"}), 400
    
    response = predictNew(data)
    # Connect to MySQL
    conn = mysql.connect()
    cursor = conn.cursor()

    for tweet, pred in response.items():
        positive = 1 if pred == 1 else 0
        negative = 1 if pred == 0 else 0

        sql = "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)"
        values = (tweet, positive, negative)
        
        cursor.execute(sql, values)
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify(response)

@app.route('/tweets', methods=['GET'])
def get_tweets():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT text, positive FROM tweets")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    response = {
        "text": [row[0] for row in rows],
        "label": [row[1] for row in rows]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

