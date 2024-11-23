import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastembed.rerank.cross_encoder import TextCrossEncoder

# Get host and port from environment variables with default values
HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
PORT = int(os.getenv("FASTAPI_PORT", "8000"))

# Get model name from environment variable
RERANKER_MODEL = os.getenv('RERANKER_MODEL', 'jinaai/jina-reranker-v1-tiny-en')

app = FastAPI()

# Initialize model
reranker_model = TextCrossEncoder(model_name=RERANKER_MODEL)

print(f"The text model {RERANKER_MODEL} is ready to use.")

class RerankerRequest(BaseModel):
    query: str
    documents: List[str]

@app.post("/rerank")
async def embed_text(request: RerankerRequest):
    try:
        scores_generator = reranker_model.rerank(request.query, request.documents)
        scores_list = list(scores_generator)
        return {
            "scores": scores_list,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthcheck")
async def healthcheck():
    """
    Health check endpoint to check if the service is up and running.
    """
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    print(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)