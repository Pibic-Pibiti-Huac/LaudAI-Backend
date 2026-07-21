import os
from openai import AsyncOpenAI
from app.services.model_util_service import (
    cot_prompt_report_message
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
            messages=cot_prompt_report_message(report),
            temperature=0.0
        )

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
    

