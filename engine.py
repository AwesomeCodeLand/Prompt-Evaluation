import threading
from models.http import GptRequest, Eval, Message, GptRequestEncoder
from log import output_log, DebugLevel, ErrLevel
from similarity import similarity_score, style_score
from wrap import chatWithOpenAI
from fluency import grammar_score, understanding_score
from divergence import divergence_score
from stores.sqlite import (
    finishEvaluationById,
    failedEvaluationById,
    update_stage_status,
    create_stage,
)
from exceptions.openaiException import (
    OpenAIException,
    SimilarityScoreException,
    FluencyScoreException,
    UnderstandScoreException,
    DivergenceScoreException,
)
import json
from dataclasses import asdict
from const_var import (
    StageInit,
    StageSimilarity,
    StageStyle,
    StageFluency,
    StageUnderstand,
    StageDivergence,
    StageStatusPadding,
    StageStatusDone,
    StageStatusFailed,
)


def do_evaluation(id: int, params: GptRequest):
    output_log(params, "do_evaluation", DebugLevel)
    # get similarity score
    try:
        output_log("create stage similarity", "do_evaluation", DebugLevel)
        create_stage(
            id,
            StageInit,
            json.dumps(params, cls=GptRequestEncoder),
            "",
            StageStatusPadding,
        )
        output_log("create stage init", "do_evaluation", DebugLevel)
        ss_score, style_score = do_similarity(id, params)
        fluency = do_fluency(id, params)
        divergence = do_divergence(id, params)
        understand = do_understand(id, params)

        # create dictionary object
        evaluation = {
            "similarity_score": ss_score,
            "style_score": style_score,
            "fluency_score": fluency,
            "divergence_score": divergence,
            "understand_score": understand,
        }

        # convert dictionary to JSON object
        evaluation_json = json.dumps(evaluation)

        finishEvaluationById(id, {"evaluation": evaluation_json})
        update_stage_status(id, StageInit, StageStatusDone)
    except OpenAIException as e:
        output_log(e, "openai", ErrLevel)
        failedEvaluationById(id, {"evaluation": "openai " + e.__str__()})
    except SimilarityScoreException as e:
        output_log(e, "similarity", ErrLevel)
        failedEvaluationById(id, {"evaluation": "similarity " + e.__str__()})
    except FluencyScoreException as e:
        output_log(e, "fluency", ErrLevel)
        failedEvaluationById(id, {"evaluation": "fluency " + e.__str__()})
    except UnderstandScoreException as e:
        output_log(e, "understand", ErrLevel)
        failedEvaluationById(id, {"evaluation": "understand " + e.__str__()})
    except DivergenceScoreException as e:
        output_log(e, "divergence", ErrLevel)
        failedEvaluationById(id, {"evaluation": "divergence " + e.__str__()})
    except Exception as e:
        output_log(e, "unknown", ErrLevel)
        failedEvaluationById(id, {"evaluation": e.__str__()})


def do_similarity(id: int, params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        similarity_score: the similarity score between the response and the standard answer
        style_score: the style score between the response and the standard answer
    """
    try:
        eval_params = params.eval
        # messages = [asdict(m) for m in eval_params.messages]
        response = chatWithOpenAI(
            params=Eval(
                model=eval_params.model,
                messages=eval_params.messages,
                temperature=eval_params.temperature,
                max_tokens=eval_params.max_tokens,
                frequency_penalty=eval_params.frequency_penalty,
                presence_penalty=eval_params.presence_penalty,
            )
        )

        ss_score = similarity_score(response, params.stand.answer)
        update_stage_status(id, StageSimilarity, StageStatusDone)

        st_score = style_score(response, params.stand.answer)
        update_stage_status(id, StageStyle, StageStatusDone)

        update_stage_status(id, StageInit, StageStatusDone)
        return ss_score, st_score
    except Exception as e:
        update_stage_status(id, StageInit, StageStatusFailed)
        raise SimilarityScoreException(e.__str__())


def do_fluency(id: int, params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        fluency_score: the fluency score of the prompt
    """
    try:
        create_stage(
            id,
            StageFluency,
            [
                params.eval.messages[0].content,
            ],
            "",
            StageStatusPadding,
        )

        result = grammar_score(
            params.eval.messages[0].content,
        )

        update_stage_status(id, StageFluency, StageStatusDone)
        return result
    except Exception as e:
        update_stage_status(id, StageFluency, StageStatusFailed)
        raise FluencyScoreException(e.__str__())


def do_understand(id: int, params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        understand_score: the understand score of the prompt
    """
    try:
        create_stage(
            id,
            StageUnderstand,
            [params.eval.messages[0].content, params.stand.answer],
            "",
            StageStatusPadding,
        )
        result = understanding_score(
            params.eval.messages[0].content,
            params.stand.answer,
        )
        update_stage_status(id, StageUnderstand, StageStatusDone)
        return result
    except Exception as e:
        update_stage_status(id, StageUnderstand, StageStatusFailed)
        raise UnderstandScoreException(e.__str__())


def do_divergence(id: int, params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        divergence_score: the divergence score of the prompt
    """
    try:
        create_stage(
            id,
            StageDivergence,
            [params.eval.messages[0].content, params.stand.answer],
            "",
            StageStatusPadding,
        )
        result = divergence_score(
            params.eval.messages[0].content,
            params.stand.answer,
        )
        update_stage_status(id, StageDivergence, StageStatusDone)
        return result
    except Exception as e:
        update_stage_status(id, StageDivergence, StageStatusFailed)
        raise DivergenceScoreException(e.__str__())
