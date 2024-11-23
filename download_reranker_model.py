import os
from fastembed.rerank.cross_encoder import TextCrossEncoder

def download_model():
    reranker_model = os.getenv('RERANKER_MODEL', 'jinaai/jina-reranker-v1-tiny-en')

    print(f"Downloading reranker model: {reranker_model}")
    TextCrossEncoder(model_name=reranker_model)
    print("Reranker model downloaded.")

if __name__ == "__main__":
    download_model()
