from flask import Flask, jsonify, render_template
from flask_cors import CORS
from controllers.plagiat_controller import plagiat_bp
from models.blacklist_model import BlacklistModel # <-- IMPORT

app = Flask(__name__)
CORS(app)

# Initialisation optionnelle de la BDD au démarrage pour être sûr
try:
    BlacklistModel()
except Exception as e:
    print(f"Erreur à l'initialisation de la base de données de liste noire: {e}")

app.register_blueprint(plagiat_bp)

@app.route('/')
def home():
    return render_template('index.html')  # renvoie le fichier HTML

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
