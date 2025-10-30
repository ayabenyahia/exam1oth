from flask import Blueprint, request, jsonify
from models.text_analyzer import TextAnalyzer
from app import db
from models.blacklist_model import Blacklist

plagiat_bp = Blueprint('plagiat', __name__)
analyzer = TextAnalyzer()

@plagiat_bp.route('/compare', methods=['POST'])
def compare_texts():
    data = request.get_json()
    text1 = data.get("text1", "")
    text2 = data.get("text2", "")
    student1 = data.get("student1", "Étudiant 1")
    student2 = data.get("student2", "Étudiant 2")

    if not text1 or not text2:
        return jsonify({"error": "Les deux textes sont requis"}), 400

    similarity = analyzer.compare(text1, text2)
    similarity_percent = round(similarity * 100, 2)

    result = {
        "student1": student1,
        "student2": student2,
        "similarity": similarity_percent
    }

    # Ajout automatique à la blacklist si similarité >= 80 %
    if similarity_percent >= 80:
        blacklist_entry = Blacklist(student1, student2, similarity_percent)
        db.session.add(blacklist_entry)
        db.session.commit()
        result["blacklisted"] = True
    else:
        result["blacklisted"] = False

    return jsonify(result)


@plagiat_bp.route('/blacklist', methods=['GET'])
def get_blacklist():
    entries = Blacklist.query.all()
    return jsonify([entry.to_dict() for entry in entries])


@plagiat_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})
