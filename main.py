import json
import uvicorn
import threading
import os
from log import output_log
from models.configure import Conf
from utils.configure import loadConfigure

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.http import GptRequest, Eval

# from tools import chatWithOpenAI
from const_var import (
    BadRequestStatusCode,
    RouterEvaluation,
    RouterSimilarity,
    RouterFluency,
    RouterUnderstand,
    RouterDivergence,
    RouterQueryStatus,
    RouterQueryStage,
    RouterStageRestart,
    RouterSpider,
    RouterHome,
    ConfigPath,
    LogInfo,
)
from similarity import similarity_score, style_score
from wrap import chatWithOpenAI
from fluency import grammar_score, understanding_score
from divergence import divergence_score
from stores.sqlite import sqliteInit, createPaddingEvaluation, getAllEvaluations
from stores.sql import sqlInit
from engine import do_evaluation, restart
from result.html import (
    outputWithHtml,
    outputStageWithHtml,
    spiderWithHtml,
    processLineWithHtml,
)
from markupsafe import Markup
from models.sql import SqlBaseModel

# sqliteInit()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

conf = Conf.from_dict()
# sqlModel
# if config_path in the environment variables, use it
config_path = os.environ.get(ConfigPath)
if config_path:
    # do something with the config_path variable
    conf = loadConfigure(config_path)

try:
    sqlModel = sqlInit(conf)
except Exception as e:
    output_log(f"sqlInit error: {e}", level="error")
    os._exit(1)


@app.post(RouterSimilarity)
def Similarity(params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        similarity
            1. similarity_score(内容相似性分数)
            2. style_score(风格相似性分数)
        fluency
            1. grammar_score(语法得分)
            2. understanding_score(可理解性得分)
        divergence
            1. diversity_score(多样性得分)
    Return a table of scores.
    """

    output_log("new evaluation", RouterEvaluation, "info")
    # check whether the prompt is None
    if params is None:
        return {"error": "params is None"}, BadRequestStatusCode

    # invoke openai chat api
    eval_params = params.eval
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

    output_log(response, "chatWithOpenAI return", "info")

    # get the similarity score
    ss_score = similarity_score(response, params.stand.answer)
    output_log(ss_score, "chatWithOpenAI return ss_score", "info")

    st_score = style_score(response, params.stand.answer)
    output_log(st_score, "chatWithOpenAI return st_score", "info")

    # fluency_score = grammar_score(params.eval.messages[0].content)
    return {
        "similarity": {"similarity_score": ss_score, "style_score": st_score},
        # "fluency_score": fluency_score,
    }, 200


# @app.route(RouterFluency, methods=["POST"])
@app.post(RouterFluency)
def Fluency(params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:

    """
    # params = request.get_json()
    fluency_score = grammar_score(
        params.eval.messages[0].content,
    )
    response_data = {
        "fluency_score": fluency_score.__dict__,
    }
    response_json = json.dumps(response_data)

    return response_json, 200


# @app.route(RouterUnderstand, methods=["POST"])
@app.post(RouterUnderstand)
def Understand(params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:

    """
    understand_score = understanding_score(
        params.eval.messages[0].content,
        params.stand.answer,
    )
    return {
        "understanding_score": understand_score,
    }, 200


# @app.route(RouterDivergence, methods=["POST"])
@app.post(RouterDivergence)
def Divergence(params: GptRequest):
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:

    """
    # params = request.get_json()
    diver_score = divergence_score(
        params.eval.messages[0].content,
        params.stand.divergence,
    )

    return {
        "divergence_score": diver_score,
    }, 200


@app.post(RouterEvaluation)
def Evaluation(name: str, params: GptRequest):
    output_log(f"new evaluation {name}", RouterEvaluation, "info")

    id = sqlModel.createEvaluation(
        {
            "name": name,
            "prompt": params.eval.messages[0].content,
        }
    )
    # id = createPaddingEvaluation(
    #     {
    #         "name": name,
    #         "prompt": params.eval.messages[0].content,
    #     }
    # )

    thread = threading.Thread(target=do_evaluation, args=(id, params))
    thread.start()
    return {
        "id": id,
    }, 200


@app.get(RouterQueryStatus, response_class=HTMLResponse)
async def QueryStatus(request: Request):
    svg, dataSource = processLineWithHtml()
    print(f"svg:{svg}")
    print(f"dataSource:{dataSource}")
    return templates.TemplateResponse(
        "processline.html",
        {"request": request, "dataSource": Markup(dataSource), "svg": Markup(svg)},
    )


@app.get(RouterQueryStage, response_class=HTMLResponse)
async def QueryStage(id: int, request: Request):
    return templates.TemplateResponse(
        "stage.html", {"request": request, "output": Markup(outputStageWithHtml(id))}
    )


@app.post(RouterStageRestart)
async def StageRestart(id: int, stageId: int):
    return restart(id, stageId)


@app.get(RouterSpider, response_class=HTMLResponse)
async def Spider(id: int, request: Request):
    return templates.TemplateResponse(
        "spiderChat.html", {"request": request, "output": Markup(spiderWithHtml(id))}
    )


@app.get(RouterHome, response_class=HTMLResponse)
async def Home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=conf.port)
