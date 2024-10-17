build docker image:
```
docker build -t fastembed-service .  
```

run:
```
docker run \
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
