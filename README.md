build docker image:
```
docker build -t fastembed-service \
  --build-arg TEXT_EMBEDDING_MODEL="BAAI/bge-small-en-v1.5" \
  --build-arg IMAGE_EMBEDDING_MODEL="Qdrant/clip-ViT-B-32-vision" \
  .
```

run:
```
docker run \
  -e TEXT_EMBEDDING_MODEL="BAAI/bge-small-en-v1.5" \
  -e IMAGE_EMBEDDING_MODEL="Qdrant/clip-ViT-B-32-vision" \
  -e FASTAPI_HOST=0.0.0.0 \
  -e FASTAPI_PORT=8000 \
  -p 8000:8000 \
  fastembed-service  
```

text embedding:
```
curl -X POST "http://localhost:8000/embed_text" \
     -H "Content-Type: application/json" \
     -d '{
       "documents": [
         "FastEmbed is lighter than Transformers & Sentence-Transformers.",
         "FastEmbed is supported by and maintained by Qdrant."
       ]
     }'
```

image embedding:
```
curl -X POST "http://localhost:8000/embed_image" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@./images/cat.jpg" \
     -F "files=@./images/solid-snake.jpg"  
```
