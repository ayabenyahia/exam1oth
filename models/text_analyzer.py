from utils.text_processor import TextProcessor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextAnalyzer:
    """
    MODEL - Analyse de similarité entre textes avec IA
    Utilise : Jaccard (basique), Cosinus (vectoriel), TF-IDF (IA/Machine Learning)
    """
    
    def __init__(self):
        self.processor = TextProcessor()
        print("✅ Analyseur de texte initialisé avec TF-IDF (IA)")
    
    
    def analyze_similarity(self, text1, text2):
        """
        Analyse la similarité avec TOUTES les méthodes disponibles
        """
        # Nettoyage
        clean_text1 = self.processor.clean_text(text1)
        clean_text2 = self.processor.clean_text(text2)
        
        # Extraction des mots
        words1 = self.processor.extract_words(clean_text1)
        words2 = self.processor.extract_words(clean_text2)
        
        # Méthode 1 : Jaccard (basique)
        jaccard = self._calculate_jaccard_similarity(words1, words2)
        
        # Méthode 2 : Cosinus basique
        cosine_basic = self._calculate_cosine_similarity(words1, words2)
        
        # Méthode 3 : TF-IDF (IA/Machine Learning)
        tfidf_sim = self._calculate_tfidf_similarity(text1, text2)
        
        # Calcul de la similarité finale (moyenne pondérée privilégiant l'IA)
        final_similarity = (jaccard * 0.3 + cosine_basic * 0.2 + tfidf_sim * 0.5)
        
        return {
            'similarity_percentage': round(final_similarity * 100, 2),
            'method_used': 'IA (TF-IDF) + Jaccard + Cosinus',
            'details': {
                'jaccard_similarity': round(jaccard * 100, 2),
                'cosine_basic': round(cosine_basic * 100, 2),
                'tfidf_similarity_ai': round(tfidf_sim * 100, 2),
                'final_weighted': round(final_similarity * 100, 2),
                'total_words_text1': len(words1),
                'total_words_text2': len(words2),
                'common_words_count': len(set(words1) & set(words2))
            }
        }
    
    
    def analyze_with_differences(self, text1, text2):
        """
        Analyse avec identification des mots communs et différents
        """
        clean_text1 = self.processor.clean_text(text1)
        clean_text2 = self.processor.clean_text(text2)
        
        words1 = set(self.processor.extract_words(clean_text1))
        words2 = set(self.processor.extract_words(clean_text2))
        
        # Mots communs
        common = words1 & words2
        
        # Mots uniques
        unique_text1 = words1 - words2
        unique_text2 = words2 - words1
        
        # Calcul de similarité avec IA
        result = self.analyze_similarity(text1, text2)
        
        return {
            'similarity_percentage': result['similarity_percentage'],
            'method_used': result['method_used'],
            'common_words': sorted(list(common)),
            'unique_text1': sorted(list(unique_text1)),
            'unique_text2': sorted(list(unique_text2)),
            'details': {
                'common_count': len(common),
                'unique_text1_count': len(unique_text1),
                'unique_text2_count': len(unique_text2),
                'ai_scores': result['details']
            }
        }
    
    
    def _calculate_jaccard_similarity(self, words1, words2):
        """
        Similarité de Jaccard (méthode basique)
        Formule: |A ∩ B| / |A ∪ B|
        """
        set1 = set(words1)
        set2 = set(words2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    
    def _calculate_cosine_similarity(self, words1, words2):
        """
        Similarité cosinus basée sur la fréquence des mots (méthode vectorielle)
        Formule: (A · B) / (||A|| × ||B||)
        """
        vocab = list(set(words1 + words2))
        
        vec1 = [words1.count(word) for word in vocab]
        vec2 = [words2.count(word) for word in vocab]
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        norm1 = sum(a ** 2 for a in vec1) ** 0.5
        norm2 = sum(b ** 2 for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    
    def _calculate_tfidf_similarity(self, text1, text2):
        """
         Similarité TF-IDF (Intelligence Artificielle / Machine Learning)
        
        TF-IDF = Term Frequency - Inverse Document Frequency
        
        Cette technique de Machine Learning pondère l'importance des mots :
        - Les mots fréquents ont moins de poids (ex: "le", "la", "de")
        - Les mots rares et significatifs ont plus de poids (ex: "algorithme", "plagiat")
        
        C'est une technique NLP (Natural Language Processing) utilisée dans :
        - Moteurs de recherche (Google, Bing)
        - Systèmes de recommandation
        - Détection de plagiat professionnelle
        """
        try:
            # Création du vectoriseur TF-IDF (modèle ML)
            vectorizer = TfidfVectorizer(
                lowercase=True,           # Normalisation
                token_pattern=r'\b\w+\b', # Extraction de tokens
                max_features=1000         # Limite de features
            )
            
            # Transformation des textes en vecteurs TF-IDF (embedding)
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            
            # Calcul de la similarité cosinus entre les vecteurs
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            print(f" Erreur TF-IDF: {e}")
            # Fallback sur méthode basique
            words1 = self.processor.extract_words(self.processor.clean_text(text1))
            words2 = self.processor.extract_words(self.processor.clean_text(text2))
            return self._calculate_jaccard_similarity(words1, words2)