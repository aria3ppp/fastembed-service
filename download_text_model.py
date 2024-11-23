import os
from fastembed import TextEmbedding

def download_model():
    text_model = os.getenv('TEXT_EMBEDDING_MODEL', 'BAAI/bge-small-en-v1.5')

    print(f"Downloading text embedding model: {text_model}")
    TextEmbedding(model_name=text_model)
    print("Text embedding model downloaded.")

if __name__ == "__main__":
    download_model()
