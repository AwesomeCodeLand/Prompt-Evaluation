import json
from models.fluency import FluencyScore
from wrap import fluency, understand
from log import output_log
from cosine_tools import IfIDFSimiliar
from prompt import GrammarPrompt_ZH, UnderstandingPrompt_ZH


def grammar_score(content):
    """
    This function is used to calculate the grammar score.
        content: the content to be checked.
    Use LanguageTool to check the grammar.
    Return a grammar score.
    """

    if content == "":
        return FluencyScore(0.0, 0.0, 0.0, 0.0)
    score = fluency(GrammarPrompt_ZH.format(content))
    output_log(score, "grammar_score", "info")
    data = json.loads(score)

    return FluencyScore(data["content"], data["grammar"], data["error"], data["logic"])


def understanding_score(content, stand):
    """
    This function is used to calculate the understanding score.
        content: the content to be checked.
    Return a understanding score.
    """
    if content == "":
        return 0.0

    myUnderStand = understand(UnderstandingPrompt_ZH.format(content))

    return IfIDFSimiliar(myUnderStand, stand)
