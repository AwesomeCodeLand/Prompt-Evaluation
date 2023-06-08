import threading
from models.http import GptRequest, Eval, Message, GptRequestEncoder, Stand
from models.fluency import FluencyScoreEncoder
from log import output_log, DebugLevel, ErrLevel
from similarity import similarity_score, style_score
from wrap import chatWithOpenAI
from fluency import grammar_score, understanding_score
from divergence import divergence_score
from stores.sqlite import (
    finishEvaluationById,
    failedEvaluationById,
    update_stage_status,
    paddingEvaluationById,
    create_stage,
    getStageById,
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
from dataBus.db import SqlDB

def do_evaluation(id: int, params: GptRequest):
    output_log(params, "do_evaluation", DebugLevel)
    # get similarity score
    try:
        output_log("create stage similarity", "do_evaluation", DebugLevel)

        SqlDB().create_stage(
            id,
            StageInit,
            json.dumps(params, cls=GptRequestEncoder),
            "",
            StageStatusPadding,
        )
        output_log("create stage init", "do_evaluation", DebugLevel)
        response, ss_score, style_score = do_similarity(id, params)
        params.response = response

        output_log("create stage similarity", "do_evaluation", DebugLevel)
        fluency = do_fluency(id, params)
        output_log("create stage fluency", "do_evaluation", DebugLevel)
        divergence = do_divergence(id, params)
        output_log("create stage divergence", "do_evaluation", DebugLevel)
        understand = do_understand(id, params)
        output_log("create stage understand", "do_evaluation", DebugLevel)

        # create dictionary object
        evaluation = {
            "similarity_score": ss_score,
            "style_score": style_score,
            "fluency_score": json.dumps(fluency, cls=FluencyScoreEncoder),
            "divergence_score": divergence,
            "understand_score": understand,
        }

        output_log(evaluation, "evaluation", DebugLevel)
        # convert dictionary to JSON object
        evaluation_json = json.dumps(evaluation)

        finishEvaluationById(id, {"evaluation": evaluation_json})
        # update_stage_status(id, StageInit, StageStatusDone)
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


def do_similarity(id: int, params: GptRequest, restart=False):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        similarity_score: the similarity score between the response and the standard answer
        style_score: the style score between the response and the standard answer
    """
    # print(f"do_similarity type: {type(params)}")
    # print(f"{params}")
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
        if restart:
            SqlDB().update_stage_status(id, StageSimilarity, StageStatusPadding)
        else:
            SqlDB().create_stage(
                id,
                StageSimilarity,
                json.dumps(params, cls=GptRequestEncoder),
                "",
                StageStatusPadding,
            )

        ss_score = similarity_score(response, params.stand.answer)
        update_stage_status(id, StageSimilarity, StageStatusDone)

        st_score = style_score(response, params.stand.answer)
        update_stage_status(id, StageStyle, StageStatusDone)

        update_stage_status(id, StageInit, StageStatusDone)
        return response, ss_score, st_score
    except Exception as e:
        print(f"do_similarity error: {e}")
        update_stage_status(id, StageInit, StageStatusFailed, e.__str__())
        raise SimilarityScoreException(e.__str__())


def do_fluency(id: int, params: GptRequest, restart=False):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        fluency_score: the fluency score of the prompt
    """
    try:
        if restart:
            SqlDB().update_stage_status(id, StageFluency, StageStatusPadding)
        else:
            create_stage(
                id,
                StageFluency,
                json.dumps(params, cls=GptRequestEncoder),
                "",
                StageStatusPadding,
            )

        result = grammar_score(
            params.eval.messages[0].content,
        )

        SqlDB().update_stage_status(id, StageFluency, StageStatusDone)
        return result
    except Exception as e:
        SqlDB().update_stage_status(id, StageFluency, StageStatusFailed)
        raise FluencyScoreException(e.__str__())


def do_understand(id: int, params: GptRequest, restart=False):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        understand_score: the understand score of the prompt
    """
    try:
        if restart:
            SqlDB().update_stage_status(id, StageUnderstand, StageStatusPadding)
        else:
            SqlDB().create_stage(
                id,
                StageUnderstand,
                json.dumps(params, cls=GptRequestEncoder),
                "",
                StageStatusPadding,
            )
        result = understanding_score(
            params.response,
            params.stand.answer,
        )

        SqlDB().update_stage_status(id, StageUnderstand, StageStatusDone)
        return result
    except Exception as e:
        SqlDB().update_stage_status(id, StageUnderstand, StageStatusFailed)
        raise UnderstandScoreException(e.__str__())


def do_divergence(id: int, params: GptRequest, restart=False):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        divergence_score: the divergence score of the prompt
    """
    try:
        if restart:
            SqlDB().update_stage_status(id, StageDivergence, StageStatusPadding)
        else:
            SqlDB().create_stage(
                id,
                StageDivergence,
                json.dumps(params, cls=GptRequestEncoder),
                "",
                StageStatusPadding,
            )
        result = divergence_score(
            params.eval.messages[0].content,
            params.stand.answer,
        )
        SqlDB().update_stage_status(id, StageDivergence, StageStatusDone)
        return result
    except Exception as e:
        SqlDB().update_stage_status(id, StageDivergence, StageStatusFailed)
        raise DivergenceScoreException(e.__str__())


def restart(eid: int, stageId: int):
    status = getStageById(eid, stageId)
    if status is None:
        raise Exception("stage not found")

    switcher = {
        StageInit: restart_init,
        StageSimilarity: restart_similarity,
        StageStyle: restart_style,
        StageFluency: restart_fluency,
        StageUnderstand: restart_understand,
        StageDivergence: restart_divergence,
        # add more cases here
    }

    # Todo
    restart_stage = switcher.get(status["stage"], restart_invalid)
    # print(f"""restart input_str: {status["input"].encode("utf-8")
    #     .decode("unicode_escape")
    #     .encode("utf-8")
    #     .decode("unicode_escape")}""")
    try:
        input_str = json.loads(json.loads(status["input"]))
        # print(f"{input_str['eval']}")
        grt = GptRequest(
            eval=Eval(
                model=input_str["eval"]["model"],
                messages=[
                    Message(
                        content=input_str["eval"]["messages"][0]["content"],
                        role=input_str["eval"]["messages"][0]["role"],
                    )
                ],
                temperature=input_str["eval"]["temperature"],
                max_tokens=input_str["eval"]["max_tokens"],
                frequency_penalty=input_str["eval"]["frequency_penalty"],
                presence_penalty=input_str["eval"]["presence_penalty"],
                n=input_str["eval"]["n"],
                stop=input_str["eval"]["stop"],
                top_n=input_str["eval"]["top_n"],
            ),
            stand=Stand(
                answer=input_str["stand"]["answer"],
            ),
        )
        if not isinstance(grt, GptRequest):
            raise Exception(
                f"invalid params type, need GptRequest, but got {type(grt)})"
            )

        print(f"{eid} {stageId} restart with {StageStatusPadding}")
        SqlDB().update_stage_status(eid, stageId, StageStatusPadding)
        paddingEvaluationById(eid)

        thread = threading.Thread(target=restart_stage, args=(eid, grt))
        thread.start()

    except Exception as e:
        print(f"restart error: {e}")


def restart_init(id: int, params: GptRequest):
    restart_similarity(id, params)


def restart_similarity(id: int, params: GptRequest):
    do_similarity(id, params, restart=True)
    restart_fluency(id, params)


def restart_style():
    pass


def restart_fluency(id: int, params: GptRequest):
    do_fluency(id, params, restart=True)
    restart_understand(id, params)


def restart_understand(id: int, params: GptRequest):
    do_understand(id, params, restart=True)
    restart_divergence(id, params)


def restart_divergence(id: int, params: GptRequest):
    do_divergence(id, params, restart=True)


def restart_invalid():
    raise Exception("invalid stage")
