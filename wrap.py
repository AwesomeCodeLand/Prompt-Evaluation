import openai
import os
from const_var import EMBEDDING_MODEL, OPENAI_API_KEY
import numpy as np
from log import output_log
from exceptions.openaiException import OpenAIException


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


def chatWithOpenAI(params):
    """
    This function is used to invoke openai chat api.
    It receives a prompt and returns a response.
    """
    # invoke openai chat api

    output_log("invoke openai chat api", "chatWithOpenAI", "info")
    openai.api_key = openaiKey()
    # try catch the error
    try:
        response = openai.ChatCompletion.create(
            model=params["model"],
            messages=params["messages"],
            max_tokens=params.get("max_tokens", 200),
            temperature=params.get("temperature", 0.7),
            top_p=params.get("top_p", 1),
            frequency_penalty=params.get("frequency_penalty", 0),
            presence_penalty=params.get("presence_penalty", 1),
            stop=params.get("stop", ""),
            n=params.get("n", 1),
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
    params = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": content,
            },
        ],
        "temperature": 0,
        "max_tokens": 2000,
        "frequency_penalty": 0,
        "presence_penalty": 2,
    }

    return chatWithOpenAI(params)


def fluency(content):
    """
    Get the content fluency data from openai.
    """
    params = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": content,
            },
        ],
        "temperature": 0,
        "max_tokens": 2000,
        "frequency_penalty": 0,
        "presence_penalty": 2,
    }

    return chatWithOpenAI(params)
