# 1
from typing import List, Optional, Dict

# 2
from uuid import uuid4

# 3
from fastapi import FastAPI, UploadFile, File, HTTPException, status

# 4
from pydantic import BaseModel, Field


# 5
app = FastAPI(
    title="GenAI Backend API",
    description="FastAPI example for chat completion and document upload",
    version="1.0.0",
)


# 6
API_PREFIX = "/api/v1"


# 7
fake_document_store: Dict[str, dict] = {}


# 8
class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int


# 9
class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="Unique user ID")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID")
    message: str = Field(..., min_length=1, max_length=4000)
    model: str = Field(default="demo-llm")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=500, ge=1, le=4000)
    document_ids: List[str] = Field(default_factory=list)


# 10
class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    model: str
    usage: TokenUsage


# 11
class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    status: str


# 12
class DocumentMetadataResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    size_bytes: int
    status: str


# 13
def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))


# 14
def generate_demo_answer(message: str, document_ids: List[str]) -> str:
    if document_ids:
        return f"Demo answer using documents {document_ids}: You asked '{message}'."
    return f"Demo answer: You asked '{message}'."


# 15
@app.get(f"{API_PREFIX}/health")
def health_check():
    return {"status": "ok"}


# 16
@app.post(
    f"{API_PREFIX}/chat/completions",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def create_chat_completion(request: ChatRequest):
    conversation_id = request.conversation_id or f"conv-{uuid4().hex[:8]}"

    for document_id in request.document_ids:
        if document_id not in fake_document_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error_code": "DOCUMENT_NOT_FOUND",
                    "message": "One or more documents were not found",
                    "document_id": document_id,
                },
            )

    answer = generate_demo_answer(
        message=request.message,
        document_ids=request.document_ids,
    )

    input_tokens = estimate_tokens(request.message)
    output_tokens = estimate_tokens(answer)

    return ChatResponse(
        conversation_id=conversation_id,
        answer=answer,
        model=request.model,
        usage=TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        ),
    )


# 17
@app.post(
    f"{API_PREFIX}/documents/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(file: UploadFile = File(...)):
    allowed_content_types = {
        "application/pdf",
        "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "UNSUPPORTED_FILE_TYPE",
                "message": "Only PDF, TXT, and DOCX files are supported",
                "content_type": file.content_type,
            },
        )

    content = await file.read()
    size_bytes = len(content)

    max_size_bytes = 5 * 1024 * 1024

    if size_bytes > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "FILE_TOO_LARGE",
                "message": "File size must be less than or equal to 5 MB",
                "size_bytes": size_bytes,
            },
        )

    document_id = f"doc-{uuid4().hex[:8]}"

    fake_document_store[document_id] = {
        "document_id": document_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": size_bytes,
        "status": "uploaded",
    }

    return DocumentUploadResponse(
        document_id=document_id,
        filename=file.filename,
        content_type=file.content_type,
        status="uploaded",
    )


# 18
@app.get(
    f"{API_PREFIX}/documents/{{document_id}}",
    response_model=DocumentMetadataResponse,
    status_code=status.HTTP_200_OK,
)
def get_document_metadata(document_id: str):
    document = fake_document_store.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "DOCUMENT_NOT_FOUND",
                "message": "Document was not found",
                "document_id": document_id,
            },
        )

    return DocumentMetadataResponse(**document)