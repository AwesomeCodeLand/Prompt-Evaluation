import logging
import sys
import os
from flask import Flask
from requests import request
from log import output_log


from openai import chatWithOpenAI
from const_var import BadRequestStatusCode, RouterEvaluation
from similarity import similarity_score

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

    
@app.route('/')
def root():
    return 'I am PE(Prompt Evaluation)!'

@app.route(RouterEvaluation, methods=['POST'])
def Evaluation():
    """
    This function is used to evaluate the performance of the prompt.
    It receives a prompt and returns a score.
    The score contains:
        similarity
            1. similarity_score(内容相似性分数)
            2. style_score(风格相似性分数)
        fluency
            1. grammar_score(语法得分)
            2. coherence_score(连贯性得分)
        divergence
            1. diversity_score(多样性得分)
    Return a table of scores.
    """

    # receive the prompt from request
    # the body of request is a json file, which is openai chat api params
    # like: 
    # {
    #   "model":{"prompt": "I am a student.", "max_tokens": 5, "temperature": 0.9},
    #   "stand":{"answer":"xxx"}
    # } 

    
    params = request.json
    output_log(params, "Evaluation", "info")

    # check whether the prompt is None
    if params is None:
        return {"error": "params is None"}, BadRequestStatusCode
    
    # get key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    # invoke openai chat api    
    response = chatWithOpenAI( params=params['model'])
    output_log(response, "chatWithOpenAI return", "info")

    # get the similarity score
    s_score = similarity_score(response, params['stand']['answer'])
    output_log(s_score, "chatWithOpenAI return s_score" , "info")
    
    return response,200

if __name__ == '__main__':
    # disable flask debug mode
    app.run(host="0.0.0.0", port=15000, debug=True, threaded=True)