import os
from fastembed import ImageEmbedding

def download_model():
    image_model = os.getenv('IMAGE_EMBEDDING_MODEL', 'Qdrant/clip-ViT-B-32-vision')

    print(f"Downloading image embedding model: {image_model}")
    ImageEmbedding(model_name=image_model)
    print("Image embedding model downloaded.")

if __name__ == "__main__":
    download_model()
