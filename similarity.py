"""
Similarity measures for comparing two content.
"""

import math
from openai import embadingWithOpenAI


def similarity_score(predice, stand):
    """
    This function is used to calculate the similarity score.
        predice: the prediced content(openai return).
        stand: the standard content(user supply).
    Use cosin similarity to calculate the similarity score.
    Return a similarity score.
    """

    # get the vector of predice and stand
    predice_vector = get_vector(predice)
    stand_vector = get_vector(stand)

    # calculate the similarity score
    similarity_score = cosine_similarity(predice_vector, stand_vector)

    return similarity_score

def get_vector(content):
    """
    This function is used to get the vector of content.
    Return a vector.
    """

    return embadingWithOpenAI(content)

def cosine_similarity(v1, v2):
    """
    This function is used to calculate the cosine similarity of two vectors.
    Return a cosine similarity.
    """

    # calculate the dot product of v1 and v2
    dot_product = 0
    for i in range(len(v1)):
        dot_product += v1[i] * v2[i]

    # calculate the norm of v1 and v2
    norm_v1 = 0
    norm_v2 = 0
    for i in range(len(v1)):
        norm_v1 += v1[i] * v1[i]
        norm_v2 += v2[i] * v2[i]
    norm_v1 = math.sqrt(norm_v1)
    norm_v2 = math.sqrt(norm_v2)

    # calculate the cosine similarity
    cosine_similarity = dot_product / (norm_v1 * norm_v2)

    return cosine_similarity