import threading
from models.http import GptRequest,Eval,Message
from log import output_log, DebugLevel
from similarity import similarity_score, style_score
from wrap import chatWithOpenAI
from fluency import grammar_score, understanding_score
from divergence import divergence_score
from stores.sqlite import finishEvaluationById,failedEvaluationById
from exceptions.openaiException import OpenAIException, SimilarityScoreException, FluencyScoreException, UnderstandScoreException, DivergenceScoreException
import json
from dataclasses import asdict

def do_evaluation(id: int, params: GptRequest):
    output_log(params,"do_evaluation",DebugLevel)
    # get similarity score
    try:
        ss_score, style_score = do_similarity(params)
        fluency = do_fluency(params)
        divergence = do_divergence(params)
        understand = do_understand(params)
        
        # create dictionary object
        evaluation = {
            "similarity_score": ss_score,
            "style_score": style_score,
            "fluency_score": fluency,
            "divergence_score": divergence,
            "understand_score": understand
        }
        
        # convert dictionary to JSON object
        evaluation_json = json.dumps(evaluation)
        
        finishEvaluationById(id,{
            "evaluation": evaluation_json
        })

    except OpenAIException as e:
        failedEvaluationById(id,{
            "evaluation": "openai "+e.__str__()
        })
    except SimilarityScoreException as e:
        failedEvaluationById(id,{
            "evaluation": "similarity "+e.__str__()
        })
    except FluencyScoreException as e:
        failedEvaluationById(id,{
            "evaluation": "fluency "+e.__str__()
        })
    except UnderstandScoreException as e:
        failedEvaluationById(id,{
            "evaluation": "understand "+e.__str__()
        })
    except DivergenceScoreException as e:
        failedEvaluationById(id,{
            "evaluation": "divergence "+e.__str__()
        })
    except Exception as e:
        # output_log(e,"do_similarity",DebugLevel)
        failedEvaluationById(id,{
            "evaluation": e.__str__()
        })

def do_similarity(params: GptRequest):
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
        response = chatWithOpenAI(params=Eval(
            model=eval_params.model,
            messages=eval_params.messages,
            temperature=eval_params.temperature,
            max_tokens=eval_params.max_tokens,
            frequency_penalty=eval_params.frequency_penalty,
            presence_penalty=eval_params.presence_penalty
        ))

        ss_score = similarity_score(response, params.stand.answer)

        st_score = style_score(response, params.stand.answer)
        

        return ss_score, st_score
    except Exception as e:
        raise SimilarityScoreException(e.__str__())

def do_fluency(params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        fluency_score: the fluency score of the prompt
    """
    try:
        result = grammar_score(
            params.eval.messages[0].content,
        )
        return result
    except Exception as e:
        raise FluencyScoreException(e.__str__())


def do_understand(params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        understand_score: the understand score of the prompt
    """
    try:
        result = understanding_score(
            params.eval.messages[0].content,
            params.stand.answer,
        ) 
        return result
    except Exception as e:
        raise UnderstandScoreException(e.__str__())

def do_divergence(params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        divergence_score: the divergence score of the prompt
    """
    try:
        result = divergence_score(
            params.eval.messages[0].content,
            params.stand.answer,
        )
        return result
    except Exception as e:
        raise DivergenceScoreException(e.__str__())