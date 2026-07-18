from fastapi import (
    APIRouter,
    Form,
    UploadFile,
    File
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
def model_analyze_report_by_text(query: MessageReportText):
    return 

@router.post(
    "/full/analyze/file",
    status_code=200,
    description="endpoint para o LLM analizar todo o laudo pelo arquivo fornecido."
)
async def upload_report(
    role: str = Form(...), # os tres pontos indica que é um campo obrigatorio
    file: UploadFile = File(...)
):
    
    # apenas os dados do arquivo recebido na requisicao, por enquanto
    return {
        "role": role,
        "filename": file.filename,
        "content_type": file.content_type
    }