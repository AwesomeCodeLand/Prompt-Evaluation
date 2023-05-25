import json
from models.fluency import FluencyScore
from wrap import fluency


def grammar_score(content):
    """
    This function is used to calculate the grammar score.
        content: the content to be checked.
    Use LanguageTool to check the grammar.
    Return a grammar score.
    """

    if content == "":
        return FluencyScore(0.0, 0.0, 0.0, 0.0)

    score = fluency(content)

    data = json.loads(score)

    return FluencyScore(data["content"], data["grammar"], data["error"], data["logic"])


def understanding_score(content):
    """
    This function is used to calculate the understanding score.
        content: the content to be checked.
    Return a understanding score.
    """
    return
