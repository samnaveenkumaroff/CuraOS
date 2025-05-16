# src/main.py
from pipeline.inference import run_inference

if __name__ == "__main__":
    texts = [
        "COVID-19 is a respiratory disease.",
        "Deep learning improves accuracy in radiology."
    ]
    embeddings = run_inference(texts)

    for i, emb in enumerate(embeddings):
        print(f"\nEmbedding for text {i+1}: {emb[:5]}...")  # Show first 5 dims
