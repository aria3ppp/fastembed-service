from fastembed import TextEmbedding, ImageEmbedding

def download_models():
    print("Downloading text embedding model...")
    TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    print("Text embedding model downloaded.")

    print("Downloading image embedding model...")
    ImageEmbedding(model_name="Qdrant/clip-ViT-B-32-vision")
    print("Image embedding model downloaded.")

if __name__ == "__main__":
    download_models()
