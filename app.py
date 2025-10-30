from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from controllers.plagiat_controller import plagiat_bp

app = Flask(__name__)
CORS(app)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plagiarism.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Importation du modèle de blacklist après création de db
from models.blacklist_model import Blacklist

# Création automatique de la base au démarrage
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Backend Flask avec blacklist fonctionne !"})

# Enregistrement du Blueprint
app.register_blueprint(plagiat_bp, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)
