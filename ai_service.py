import os

import requests
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.5"))
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "500"))


def generate_ai_response(user_text: str, history=None) -> str:
    if not OPENROUTER_API_KEY:
        return "Ошибка: OPENROUTER_API_KEY не найден в .env"

    if history is None:
        history = []

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = [
        {
            "role": "system",
            "content": (
                "Ты полезный Telegram AI assistant. "
                "Отвечай кратко, ясно и по делу."
            ),
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_text,
        }
    )

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "temperature": AI_TEMPERATURE,
        "max_tokens": AI_MAX_TOKENS,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30,
        )

        if not response.ok:
            return (
                f"Ошибка API-запроса: {response.status_code}\n"
                f"Ответ OpenRouter: {response.text}"
            )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as error:
        return f"Ошибка API-запроса: {error}"

    except KeyError:
        return "Ошибка: неожиданный формат ответа от OpenRouter."