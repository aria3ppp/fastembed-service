import os
from fastembed import TextEmbedding, ImageEmbedding

def download_models():
    text_model = os.getenv('TEXT_EMBEDDING_MODEL', 'BAAI/bge-small-en-v1.5')
    image_model = os.getenv('IMAGE_EMBEDDING_MODEL', 'Qdrant/clip-ViT-B-32-vision')

    print(f"Downloading text embedding model: {text_model}")
    TextEmbedding(model_name=text_model)
    print("Text embedding model downloaded.")

    print(f"Downloading image embedding model: {image_model}")
    ImageEmbedding(model_name=image_model)
    print("Image embedding model downloaded.")

if __name__ == "__main__":
    download_models()
