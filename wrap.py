import openai
import os
from const_var import EMBEDDING_MODEL, OPENAI_API_KEY
import numpy as np
from log import output_log
from exceptions.openaiException import OpenAIException
from models.http import Eval


def openaiKey():
    return os.getenv(OPENAI_API_KEY)


def embadingWithOpenAI(content):
    """
    The openai Embedding API is used to get the vector of content.
    Return a vector.
    """

    openai.api_key = openaiKey()
    response = openai.Embedding.create(model=EMBEDDING_MODEL, input=content)

    return [np.array(data["embedding"]) for data in response["data"]]


def chatWithOpenAI(params:Eval):
    """
    This function is used to invoke openai chat api.
    It receives a prompt and returns a response.
    """
    # invoke openai chat api

    output_log(type(params), "chatWithOpenAI", "info")
    
    # if 'max_tokens' not in params or params['max_tokens'] is None:
    #     params['max_tokens'] = 200
    # if 'temperature' not in params or params['temperature'] is None:
    #     params['temperature'] = 0.7
    # # check top_n whether exist in params
    # if 'top_n' not in params or params['top_n'] is None:
    #     params['top_n'] = 1
    # if 'frequency_penalty' not in params or params['frequency_penalty'] is None:
    #     params['frequency_penalty'] = 0
    # if 'presence_penalty' not in params or params['presence_penalty'] is None:
    #     params['presence_penalty'] = 0
    # if 'stop' not in params or params['stop'] is None:
    #     params['stop'] = ""
    # if 'n' not in params or params['n'] is None:
    #     params['n'] = 1
    # check frequency_penalty whether exist in params
    openai.api_key = openaiKey()
    # try catch the error
    try:
        output_log(params, "openai chat api params", "info")
        # response = openai.ChatCompletion.create(
        #     model=params['model'],
        #     messages=params['messages'],
        #     # check whether the max_tokens is None
        #     # if it is None, set it to 200
        #     max_tokens=params['max_tokens'] ,
        #     temperature = params['temperature'] ,
        #     top_p = params['top_n'] ,
        #     frequency_penalty = params['frequency_penalty'] ,
        #     presence_penalty= params['presence_penalty'] ,
        #     stop = params['stop'] ,
        #     n = params['n'] ,
        #     stream=False,
        # )
        response = openai.ChatCompletion.create(
            model=params.model,
            messages=params.messages,
            # check whether the max_tokens is None
            # if it is None, set it to 200
            max_tokens=params.max_tokens,
            temperature = params.temperature,
            top_p = params.top_n ,
            frequency_penalty = params.frequency_penalty,
            presence_penalty= params.presence_penalty,
            stop = params.stop,
            n = params.n,
            stream=False,
        )

        output_log(response, "openai chat api response", "info")
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        output_log(e, "openai chat api error", "error")
        raise OpenAIException(e)


def style(content):
    """
    Get the content style data from openai.
    """
    # params = {
    #     "model": "gpt-3.5-turbo",
    #     "messages": [
    #         {"role": "system", "content": ""},
    #         {
    #             "role": "user",
    #             "content": content,
    #         },
    #     ],
    #     "temperature": 0,
    #     "max_tokens": 2000,
    #     "frequency_penalty": 0,
    #     "presence_penalty": 2,
    # }

    params=Eval(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": content,
            },
        ],
        temperature=0,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=2
    )
    return chatWithOpenAI(params=params)


def fluency(content):
    """
    Get the content fluency data from openai.
    """
    # params = {
    #     "model": "gpt-3.5-turbo",
    #     "messages": [
    #         {"role": "system", "content": ""},
    #         {
    #             "role": "user",
    #             "content": content,
    #         },
    #     ],
    #     "temperature": 0,
    #     "max_tokens": 2000,
    #     "frequency_penalty": 0,
    #     "presence_penalty": 2,
    # }

    params=Eval(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": content,
            },
        ],
        temperature=0,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=2
    )
    return chatWithOpenAI(params=params)


def understand(content):
    """
    Get the content understand data from openai.
    """

    params=Eval(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": content,
            },
        ],
        temperature=0,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=2
    )
    return chatWithOpenAI(params=params)


def divergence(content):
    """
    Get the content divergence data from openai.
    """

    params=Eval(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": content,
            },
        ],
        temperature=0,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=2
    )
    return chatWithOpenAI(params=params)