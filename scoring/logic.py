from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_score(essay_text, reference_text, min_score=0, max_score=100):
    if not essay_text or not reference_text:
        return min_score

    # Create the Document-Term Matrix
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([reference_text, essay_text])

    # Compute Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # Map similarity (0-1) to score range
    score_range = max_score - min_score
    final_score = min_score + (cosine_sim * score_range)

    return round(final_score, 2)
