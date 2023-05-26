# Prompt-Evaluation

## How to evaulation prompt?

There are three parts to the evaluation prompt:

1. Similarity
2. Fluency
3. Divergence

In the `Similarity` section, it will calculate the `similarity score` and `style score`. The `similarity score` measures how similar the OpenAI predicted content is to the standard content. It use IF-IDF algorithm.

In the `Fluency` section, it will calculate the `grammar score` and `readability score`. The `grammar score` measures how fluent the OpenAI predicted content is. It use OpenAI to check the grammar. The `readability score` measures how easy the OpenAI predicted content is to read. It use Flesch–Kincaid readability tests.

In the `Divergence` section, it will calculate the `divergence score`. The `divergence score` measures how different the OpenAI predicted content is to the standard content. We say that the OpenAI predicted content is divergent if it is different from the standard content. It use OpenAI to check the divergence.

## Example

### Similarity

```json
{
    "eval": {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "I am a student. What about you?"
            }
        ],
        "temperature": 0,
        "max_tokens": 2300,
        "frequency_penalty": 0,
        "presence_penalty": 2
    },
    "stand": {
        "answer": "As an AI language model, I don't have a physical form or occupation like humans do. My purpose is to assist and communicate with users through text-based conversations."
    }
}
```

## Fluency

```json
{
    "eval": {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "I am a student. What about you?"
            }
        ],
        "temperature": 0,
        "max_tokens": 2300,
        "frequency_penalty": 0,
        "presence_penalty": 2
    }
}
```

## Divergence

```json
{
    "eval": {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "As an AI language model, I don't have a physical form or occupation like humans do. My purpose is to assist and communicate with users through voice-based conversations."
            }
        ],
        "temperature": 0,
        "max_tokens": 2300,
        "frequency_penalty": 0,
        "presence_penalty": 2
    },
    "stand": {
        "answer": "As an AI language model, I don't have a physical form or occupation like humans do. My purpose is to assist and communicate with users through text-based conversations."
    }
}
```

