import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastembed import TextEmbedding

# Get host and port from environment variables with default values
HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
PORT = int(os.getenv("FASTAPI_PORT", "8000"))

# Get model name from environment variable
TEXT_MODEL = os.getenv('TEXT_EMBEDDING_MODEL', 'BAAI/bge-small-en-v1.5')

app = FastAPI()

# Initialize embedding model
text_embedding_model = TextEmbedding(model_name=TEXT_MODEL)

print(f"The text model {TEXT_MODEL} is ready to use.")

class TextEmbeddingRequest(BaseModel):
    documents: List[str]

@app.post("/embed_text")
async def embed_text(request: TextEmbeddingRequest):
    try:
        embeddings_generator = text_embedding_model.embed(request.documents)
        embeddings_list = list(embeddings_generator)
        embedding_size = len(embeddings_list[0]) if embeddings_list else 0
        return {
            "embeddings": [emb.tolist() for emb in embeddings_list],
            "embedding_size": embedding_size
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