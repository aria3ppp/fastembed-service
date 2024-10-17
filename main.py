import os
from typing import List
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import numpy as np
from fastembed import TextEmbedding, ImageEmbedding
from PIL import Image, UnidentifiedImageError

# Get host and port from environment variables with default values
HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
PORT = int(os.getenv("FASTAPI_PORT", "8000"))

app = FastAPI()

# Initialize embedding models
text_embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
image_embedding_model = ImageEmbedding(model_name="Qdrant/clip-ViT-B-32-vision")

print("The text model BAAI/bge-small-en-v1.5 is ready to use.")
print("The image model Qdrant/clip-ViT-B-32-vision is ready to use.")

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

@app.post("/embed_image")
async def embed_image(files: List[UploadFile] = File(...)):
    try:
        image_data = []
        for file in files:
            contents = await file.read()
            try:
                img = Image.open(io.BytesIO(contents))
                image_data.append(img)
            except UnidentifiedImageError:
                raise HTTPException(status_code=400, detail=f"File '{file.filename}' is not a valid image file")

        image_embeddings_generator = image_embedding_model.embed(image_data)
        image_embeddings_list = list(image_embeddings_generator)
        embedding_size = len(image_embeddings_list[0]) if image_embeddings_list else 0

        return {
            "embeddings": [emb.tolist() for emb in image_embeddings_list],
            "embedding_size": embedding_size
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)
