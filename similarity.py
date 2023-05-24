"""
Similarity measures for comparing two content.
"""

from wrap import embadingWithOpenAI, style
from prompt import StylePrompt
from log import output_log
from cosine_tools import IfIDFSimiliar
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np


def similarity_score(predice, stand):
    """
    This function is used to calculate the similarity score.
        predice: the prediced content(openai return).
        stand: the standard content(user supply).
    Use cosin similarity to calculate the similarity score.
    Return a similarity score.
    """

    # get the vector of predice and stand
    output_log(predice, "predice_similarity_score", "info")
    output_log(stand, "stand_similarity_score", "info")

    return IfIDFSimiliar(predice, stand)


def style_score(predice, stand):
    """
    This function is used to calculate the style score.
        predice: the prediced content(openai return).
        stand: the standard content(user supply).
    Use cosin similarity to calculate the style score.
    Return a style score.
    """

    # warp the predice and stand with StylePrompt
    predice = predice.replace(" ", "").replace("\n", "")
    stand = stand.replace(" ", "").replace("\n", "")

    if predice == stand:
        return 1.0
    if predice != "" and stand == "":
        return 0.0
    if predice == "" and stand != "":
        return 0.0

    if predice != "":
        predice = StylePrompt.format(predice)
    if stand != "":
        stand = StylePrompt.format(stand)

    predice_sytle = style(predice)
    stand_sytle = style(stand)
    output_log(predice_sytle, "predice_sytle", "info")
    output_log(stand_sytle, "stand_sytle", "info")

    # calculate the style score
    return cosine_similar(predice_sytle, stand_sytle)


def get_vector(content):
    """
    This function is used to get the vector of content.
    Return a vector.
    """

    return embadingWithOpenAI(content)


def cosine_similar(vector1, vector2):
    """
    This function is used to calculate the cosine similarity of two strings use IF-IDF.
    Return a cosine similarity.
    """
    v1 = vector1.split()
    v2 = vector2.split()

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([v1, v2])
    tfidf_array = tfidf.toarray()
    return cosine_similarity(
        tfidf_array[0].reshape(1, -1), tfidf_array[1].reshape(1, -1)
    )[0][0]
