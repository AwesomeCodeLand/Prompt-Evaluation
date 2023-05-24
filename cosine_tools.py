from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def IfIDFSimiliar(string1, string2):
    # Tokenize the strings
    tokens1 = string1.lower().split()
    tokens2 = string2.lower().split()

    # Calculate the TF-IDF vectors of the strings
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([string1, string2])
    tfidf_array = tfidf.toarray()

    # Calculate the cosine similarity between the TF-IDF vectors
    similarity_score = cosine_similarity(
        tfidf_array[0].reshape(1, -1), tfidf_array[1].reshape(1, -1)
    )[0][0]

    return similarity_score
