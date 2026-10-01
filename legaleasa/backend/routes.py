from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):

    document_type: str = Field(
        min_length=2,
        max_length=120
    )

    parties: str = Field(
        min_length=2,
        max_length=3000
    )

    terms: str = Field(
        min_length=2,
        max_length=8000
    )

    effective_date: str = Field(
        min_length=2,
        max_length=100
    )

    jurisdiction: str = Field(
        default="Not specified",
        max_length=200
    )

    additional_instructions: str = Field(
        default="",
        max_length=3000
    )

class DocumentResponse(BaseModel):

    document: str
    model: str
    demo_mode: bool

@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(request: DocumentRequest):

    try:

        result = generator.generate_document(
            **request.model_dump()
        )

        return DocumentResponse(**result)

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {error}"
        )