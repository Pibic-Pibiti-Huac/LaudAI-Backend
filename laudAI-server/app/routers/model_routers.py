import json
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi.responses import StreamingResponse
from app.schemas.auth_schemas import TokenProviderData
from app.schemas.model_schemas import (
    MessageCorrectReport,
    MessageModel,
    MessageModelFullAnalyzeResponse,
    MessageModelResponse,
    MessageReportText
)
from app.services.model_service import ModelService 
from app.services.auth_service import verify_token

router = APIRouter(
    prefix="/agent",
)

service = ModelService()

@router.post(
    "/full/analyze/text",
    status_code=200,
    description="endpoint para o LLM analizar todo o laudo pelo texto fornecido."
)
async def model_analyze_report_by_text(query: MessageReportText, token_data: TokenProviderData = Depends(verify_token)) -> MessageModelFullAnalyzeResponse:
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

@router.post(
    "/message",
    status_code=200,
    description="endpoint para o LLM responder normalmente."
)
async def model_chat(query: MessageModel,  token_data: TokenProviderData = Depends(verify_token)) -> MessageModelResponse:
    content, thinking = await service.default_chat(
        query.prompt,
        query.history,
        query.laudo_text,
    )

    return MessageModelResponse(
        role="assistant",
        response=content,
        thinking=thinking
    )

@router.post(
    "/message/stream",
    status_code=200,
    description="endpoint para o LLM responder com streaming (SSE)."
)
async def model_chat_stream(query: MessageModel, token_data: TokenProviderData = Depends(verify_token)):
    return StreamingResponse(
        service.default_chat_stream(query.prompt, query.history, query.laudo_text),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )

@router.post(
    "/correct/report",
    status_code=200,
    description="endpoint para gerar o laudo corrigido, seguindo os criterios de avaliacao e usando a avaliacao inicial como contexto interno."
)
async def model_correct_report(query: MessageCorrectReport, token_data: TokenProviderData = Depends(verify_token)):
    return StreamingResponse(
        service.correct_report_stream(query.laudo_text, query.evaluation),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
