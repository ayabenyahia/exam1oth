from flask import Blueprint, request, jsonify
from models.text_analyzer import TextAnalyzer

# Création du Blueprint
plagiat_bp = Blueprint('plagiat', __name__)

# Instance du modèle
analyzer = TextAnalyzer()


# ========================================
# ROUTE 1 : Health Check
# ========================================
@plagiat_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Vérifie que l'API fonctionne
    Test: GET http://localhost:5000/api/health
    """
    return jsonify({
        'status': 'OK',
        'message': 'API de détection de plagiat opérationnelle',
        'version': '1.0'
    }), 200


# ========================================
# ROUTE 2 : Nettoyage de texte uniquement
# ========================================
@plagiat_bp.route('/api/clean-text', methods=['POST'])
def clean_text():
    """
    Nettoie un texte (minuscules, sans ponctuation, espaces normalisés)
    Test Postman:
    POST http://localhost:5000/api/clean-text
    Body: {"text": "Bonjour, Comment ça va?"}
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Le champ "text" est requis',
                'success': False
            }), 400
        
        text = data['text']
        
        if not text.strip():
            return jsonify({
                'error': 'Le texte ne peut pas être vide',
                'success': False
            }), 400
        
        # Nettoyage
        cleaned = analyzer.processor.clean_text(text)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'cleaned_text': cleaned
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 3 : Extraction de mots uniquement
# ========================================
@plagiat_bp.route('/api/extract-words', methods=['POST'])
def extract_words():
    """
    Extrait les mots d'un texte
    Test Postman:
    POST http://localhost:5000/api/extract-words
    Body: {"text": "Le chat mange une souris"}
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Le champ "text" est requis',
                'success': False
            }), 400
        
        text = data['text']
        
        if not text.strip():
            return jsonify({
                'error': 'Le texte ne peut pas être vide',
                'success': False
            }), 400
        
        # Nettoyage puis extraction
        cleaned = analyzer.processor.clean_text(text)
        words = analyzer.processor.extract_words(cleaned)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'cleaned_text': cleaned,
            'words': words,
            'word_count': len(words)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 4 : Similarité Jaccard uniquement
# ========================================
@plagiat_bp.route('/api/jaccard-similarity', methods=['POST'])
def jaccard_similarity():
    """
    Calcule uniquement la similarité de Jaccard
    Test Postman:
    POST http://localhost:5000/api/jaccard-similarity
    Body: {"text1": "...", "text2": "..."}
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Nettoyage
        clean1 = analyzer.processor.clean_text(text1)
        clean2 = analyzer.processor.clean_text(text2)
        
        # Extraction
        words1 = analyzer.processor.extract_words(clean1)
        words2 = analyzer.processor.extract_words(clean2)
        
        # Calcul Jaccard
        jaccard = analyzer._calculate_jaccard_similarity(words1, words2)
        
        return jsonify({
            'success': True,
            'method': 'Jaccard Similarity',
            'similarity_percentage': round(jaccard * 100, 2),
            'details': {
                'words_text1': len(words1),
                'words_text2': len(words2),
                'common_words': len(set(words1) & set(words2)),
                'total_unique_words': len(set(words1) | set(words2))
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 5 : Similarité Cosinus uniquement
# ========================================
@plagiat_bp.route('/api/cosine-similarity', methods=['POST'])
def cosine_similarity():
    """
    Calcule uniquement la similarité cosinus
    Test Postman:
    POST http://localhost:5000/api/cosine-similarity
    Body: {"text1": "...", "text2": "..."}
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Nettoyage
        clean1 = analyzer.processor.clean_text(text1)
        clean2 = analyzer.processor.clean_text(text2)
        
        # Extraction
        words1 = analyzer.processor.extract_words(clean1)
        words2 = analyzer.processor.extract_words(clean2)
        
        # Calcul Cosinus
        cosine = analyzer._calculate_cosine_similarity(words1, words2)
        
        return jsonify({
            'success': True,
            'method': 'Cosine Similarity',
            'similarity_percentage': round(cosine * 100, 2),
            'details': {
                'words_text1': len(words1),
                'words_text2': len(words2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 6 : Mots communs uniquement
# ========================================
@plagiat_bp.route('/api/common-words', methods=['POST'])
def common_words():
    """
    Identifie les mots communs entre deux textes
    Test Postman:
    POST http://localhost:5000/api/common-words
    Body: {"text1": "...", "text2": "..."}
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Nettoyage et extraction
        clean1 = analyzer.processor.clean_text(text1)
        clean2 = analyzer.processor.clean_text(text2)
        
        words1 = set(analyzer.processor.extract_words(clean1))
        words2 = set(analyzer.processor.extract_words(clean2))
        
        # Mots communs
        common = words1 & words2
        
        return jsonify({
            'success': True,
            'common_words': sorted(list(common)),
            'common_count': len(common)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 7 : Mots uniques uniquement
# ========================================
@plagiat_bp.route('/api/unique-words', methods=['POST'])
def unique_words():
    """
    Identifie les mots uniques à chaque texte
    Test Postman:
    POST http://localhost:5000/api/unique-words
    Body: {"text1": "...", "text2": "..."}
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Nettoyage et extraction
        clean1 = analyzer.processor.clean_text(text1)
        clean2 = analyzer.processor.clean_text(text2)
        
        words1 = set(analyzer.processor.extract_words(clean1))
        words2 = set(analyzer.processor.extract_words(clean2))
        
        # Mots uniques
        unique1 = words1 - words2
        unique2 = words2 - words1
        
        return jsonify({
            'success': True,
            'unique_text1': sorted(list(unique1)),
            'unique_text2': sorted(list(unique2)),
            'unique_count_text1': len(unique1),
            'unique_count_text2': len(unique2)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 8 : Comparaison complète (comme avant)
# ========================================
@plagiat_bp.route('/api/compare', methods=['POST'])
def compare_texts():
    """
    Comparaison complète avec toutes les métriques
    Test Postman:
    POST http://localhost:5000/api/compare
    Body: {"text1": "...", "text2": "..."}
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Analyse complète
        result = analyzer.analyze_similarity(text1, text2)
        
        return jsonify({
            'success': True,
            'similarity_percentage': result['similarity_percentage'],
            'method_used': result['method_used'],
            'details': result['details']
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500


# ========================================
# ROUTE 9 : Comparaison avec highlight (comme avant)
# ========================================
@plagiat_bp.route('/api/compare-with-highlight', methods=['POST'])
def compare_with_highlight():
    """
    Comparaison avec mise en évidence des différences
    Test Postman:
    POST http://localhost:5000/api/compare-with-highlight
    Body: {"text1": "...", "text2": "..."}
    """
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({
                'error': 'Les champs "text1" et "text2" sont requis',
                'success': False
            }), 400
        
        text1 = data['text1']
        text2 = data['text2']
        
        if not text1.strip() or not text2.strip():
            return jsonify({
                'error': 'Les textes ne peuvent pas être vides',
                'success': False
            }), 400
        
        # Analyse avec différences
        result = analyzer.analyze_with_differences(text1, text2)
        
        return jsonify({
            'success': True,
            'similarity_percentage': result['similarity_percentage'],
            'common_words': result['common_words'],
            'unique_text1': result['unique_text1'],
            'unique_text2': result['unique_text2'],
            'details': result['details']
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500