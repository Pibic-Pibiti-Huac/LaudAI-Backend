import os
import json
from openai import AsyncOpenAI
from app.services.model_util_service import (
    cot_prompt_report_message,
    correct_report_prompt_model,
    default_prompt_model
)

class ModelService:
    """
    Esse service vai fazer as requisicoes com o modelo da aplicacao e vai slavar o regsitro da conversa.
    """

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            base_url=os.environ["LLAMACPP_BASE_URL"] + "/v1",
            api_key=os.environ["LLAMACPP_API_KEY"],
        )

    async def report_analyze_by_text(self, report: str):
        return await self.chat(
            messages=cot_prompt_report_message(report, examples_on=False),
            temperature=0.0
        )

    async def default_chat(self, chat_user_text: str, history: list[dict] | None = None, laudo_text: str | None = None):
            return await self.chat(
                messages=default_prompt_model(chat_user_text, history, laudo_text)
            )

    async def default_chat_stream(self, chat_user_text: str, history: list[dict] | None = None, laudo_text: str | None = None):
        messages = default_prompt_model(chat_user_text, history, laudo_text)
        stream = await self.client.chat.completions.create(
            model="qwen3-8b",
            messages=messages,
            temperature=0.7,
            stream=True,
        )
        async for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    async def correct_report_stream(self, laudo_text: str, evaluation: dict | None = None):
        messages = correct_report_prompt_model(laudo_text, evaluation)
        stream = await self.client.chat.completions.create(
            model="qwen3-8b",
            messages=messages,
            temperature=0.0,
            stream=True,
        )
        async for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    async def chat(self, messages: list[dict], model: str = "qwen3-8b", temperature: float = 0.7):
        """
        Função geral de chat, as outras funções desse service devem chamar essa função internamnete.
        """
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        message = response.choices[0].message
        thinking = getattr(message, "reasoning_content", None)
        content = message.content

        return content, thinking
    

