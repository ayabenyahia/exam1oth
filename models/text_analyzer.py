from utils.text_processor import clean_and_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TextAnalyzer:
    def __init__(self):
        pass

    def jaccard_similarity(self, text1, text2):
        set1 = set(clean_and_tokenize(text1))
        set2 = set(clean_and_tokenize(text2))
        if not set1 or not set2:
            return 0.0
        return len(set1 & set2) / len(set1 | set2)

    def cosine_similarity_score(self, text1, text2):
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([text1, text2])
        cos_sim = cosine_similarity(tfidf[0:1], tfidf[1:2])
        return float(cos_sim[0][0])

    def compare(self, text1, text2):
        # Utilise la moyenne des deux méthodes
        jaccard = self.jaccard_similarity(text1, text2)
        cosine = self.cosine_similarity_score(text1, text2)
        return (jaccard + cosine) / 2
