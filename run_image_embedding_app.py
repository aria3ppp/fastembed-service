import os
from typing import List
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastembed import ImageEmbedding
from PIL import Image, UnidentifiedImageError

# Get host and port from environment variables with default values
HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
PORT = int(os.getenv("FASTAPI_PORT", "8000"))

# Get model name from environment variable
IMAGE_MODEL = os.getenv('IMAGE_EMBEDDING_MODEL', 'Qdrant/clip-ViT-B-32-vision')

app = FastAPI()

# Initialize embedding model
image_embedding_model = ImageEmbedding(model_name=IMAGE_MODEL)

print(f"The image model {IMAGE_MODEL} is ready to use.")

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