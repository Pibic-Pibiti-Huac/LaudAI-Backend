from click import prompt
from pydantic import BaseModel, ConfigDict

class MessageReportText(BaseModel):
    role: str
    report: str

class ReportAnalyze(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        frozen=True
    )

    extracao: dict[str, str]
    avaliacao: dict[str, str]
    notas: dict[str, int]


class MessageModelFullAnalyzeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,      # Permite validar a partir de objetos (ex: SQLAlchemy/ORM)
        str_strip_whitespace=True, # Remove espaços em branco antes/depois das strings
        frozen=True                # Opcional: Torna o modelo imutável (bom para respostas)
    )

    role: str
    thinking: str | None
    feedback: ReportAnalyze | None

class MessageModel(BaseModel):
    role: str
    prompt: str
    history: list[dict] = []
    laudo_text: str = ""

class MessageModelResponse(BaseModel):
    role: str
    response: str | None
    thinking: str | None