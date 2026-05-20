from groq import Groq
from config import get_settings
from functools import lru_cache


@lru_cache
def get_llm_client() -> Groq:
    settings = get_settings()
    return Groq(api_key=settings.groq_api_key)


def generate(prompt: str) -> str:
    settings = get_settings()
    client = get_llm_client()
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content
