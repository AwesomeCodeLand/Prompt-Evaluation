from wrap import divergence
from prompt import DivergencePrompt_ZH


def divergence_score(contentA, contentB):
    """
    This function is used to calculate the divergence score.
        contentA: the contentA.
        contentB: the contentB.
    Use cosin similarity to calculate the divergence score.
    Return a divergence score.
    """

    if contentA == "":
        return 1.0
    if contentB == "":
        return 1.0

    return divergence(DivergencePrompt_ZH.format(contentA, contentB))
