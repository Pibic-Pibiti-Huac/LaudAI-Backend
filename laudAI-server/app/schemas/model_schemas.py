from pydantic import BaseModel, ConfigDict

class MessageReportText(BaseModel):
    role: str
    report: str

class MessageModelFullAnalyzeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,      # Permite validar a partir de objetos (ex: SQLAlchemy/ORM)
        str_strip_whitespace=True, # Remove espaços em branco antes/depois das strings
        frozen=True                # Opcional: Torna o modelo imutável (bom para respostas)
    )

    role: str
    stars: int
    feedback: str