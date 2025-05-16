# src/pipeline/inference.py
from .embedding import load_model, get_embedding

def run_inference(input_texts):
    model = load_model()
    embeddings = [get_embedding(model, text) for text in input_texts]
    return embeddings
