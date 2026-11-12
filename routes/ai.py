import os
import httpx
import traceback

from dotenv import load_dotenv
from fastapi import Request, HTTPException, APIRouter, Depends
from groq import AsyncGroq
from pydantic import BaseModel, Field

from middlewares.jwt_token import check_token

router = APIRouter(
  prefix="/ai", 
  dependencies=[Depends(check_token)],
  tags=["AI"]
)

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("A varável da API não existe")

http_client = httpx.AsyncClient(verify=False)

groq_client = AsyncGroq(
  api_key=os.getenv("GROQ_API_KEY"),
  http_client=http_client
)

class ChatRequest(BaseModel):
  prompt: str

historico_contexto = []
@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
  historico_contexto.append({"role": "user", "content": request.prompt})

  try:
      completion = await groq_client.chat.completions.create(
          model="openai/gpt-oss-120b",
          messages=historico_contexto,
          temperature=0.7
      )
        
      historico_contexto.append({"role": "assistant", "content": request.prompt})
                
      return {"response": completion.choices[0].message.content}

  except Exception as e:
      traceback.print_exc()
      raise HTTPException(status_code=500, detail=str(e))