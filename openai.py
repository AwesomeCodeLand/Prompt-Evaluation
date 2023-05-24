import os
import openai


def openAIKey():
    return os.getenv("OPENAI_API_KEY")


def embadingWithOpenAI(content):
    """
    The OpenAI Embedding API is used to get the vector of content.
    Return a vector.
    """

    openai.api_key = openAIKey()

    response = openai.Embedding.create(engine="text-embedding-ada-002", prompt=content)

    # check response status code and return response
    if response["code"] != 200:
        return response

    # check if response contains error
    if "error" in response:
        return response["error"]

    return response["embedding"]


def chatWithOpenAI(params):
    """
    The OpenAI Chat API is used to generate a response to a user's message.

    """
    openai.api_key = openAIKey()

    response = openai.ChatCompletion.create(
        model=params["model"],
        messages=params["messages"],
        max_tokens=params["max_tokens"],
        temperature=params["temperature"],
        top_p=params["top_p"],
        frequency_penalty=params["frequency_penalty"],
        presence_penalty=params["presence_penalty"],
        stop=params["stop"],
        n=params["n"],
        stream=False,
    )

    # check response status code and return response
    if response["code"] != 200:
        return response

    # check if response contains error
    if "error" in response:
        return response["error"]

    return response["choices"][0]["message"]["content"]


def style(content):
    """
    Get the content style data from OpenAI.
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
