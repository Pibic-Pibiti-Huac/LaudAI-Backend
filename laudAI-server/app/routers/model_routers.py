import json
from fastapi import (
    APIRouter,
    HTTPException
)
from app.schemas.model_schemas import (
    MessageModelFullAnalyzeResponse,
    MessageReportText
)
from app.services.model_service import ModelService 

router = APIRouter(
    prefix="/agent",
)

service = ModelService()

@router.post(
    "/full/analyze/text",
    status_code=200,
    description="endpoint para o LLM analizar todo o laudo pelo texto fornecido."
)
async def model_analyze_report_by_text(query: MessageReportText) -> MessageModelFullAnalyzeResponse:
    content, thinking = await service.report_analyze_by_text(query.report)

    try:
        parsed_content = json.loads(content) # type: ignore
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="O modelo retornou uma resposta em formato inválido."
        )

    return MessageModelFullAnalyzeResponse(
        role="assistant",
        feedback=parsed_content,
        thinking=thinking
    )