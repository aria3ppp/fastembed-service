build docker image:
```
docker build -t fastembed-text \
  --build-arg TEXT_EMBEDDING_MODEL="BAAI/bge-small-en-v1.5" \
  --file ./docker/DockerfileTextEmbedding
  .

docker build -t fastembed-image \
  --build-arg IMAGE_EMBEDDING_MODEL="Qdrant/clip-ViT-B-32-vision" \
  --file ./docker/DockerfileImageEmbedding
  .

docker build -t fastembed-reranker \
  --build-arg RERANKER_MODEL="jinaai/jina-reranker-v1-tiny-en" \
  --file ./docker/DockerfileReranker
  .
```

run:
```
docker run \
  -e TEXT_EMBEDDING_MODEL="BAAI/bge-small-en-v1.5" \
  -e FASTAPI_HOST=0.0.0.0 \
  -e FASTAPI_PORT=8000 \
  -p 8000:8000 \
  fastembed-text

docker run \
  -e IMAGE_EMBEDDING_MODEL="Qdrant/clip-ViT-B-32-vision" \
  -e FASTAPI_HOST=0.0.0.0 \
  -e FASTAPI_PORT=8000 \
  -p 8001:8000 \
  fastembed-image

docker run \
  -e RERANKER_MODEL="jinaai/jina-reranker-v1-tiny-en" \
  -e FASTAPI_HOST=0.0.0.0 \
  -e FASTAPI_PORT=8000 \
  -p 8002:8000 \
  fastembed-reranker
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
curl -X POST "http://localhost:8001/embed_image" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@./images/cat.jpg" \
     -F "files=@./images/solid-snake.jpg"  
```

reranker:
```
curl -X POST "http://localhost:8000/rerank" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Who is maintaining Qdrant?",
       "documents": [
         "This is built to be faster and lighter than other embedding libraries e.g. Transformers, Sentence-Transformers, etc.",
         "fastembed is supported by and maintained by Qdrant."
       ]
     }'
```