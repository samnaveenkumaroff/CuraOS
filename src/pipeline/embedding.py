# src/pipeline/embedding.py
from sentence_transformers import SentenceTransformer

def load_model(model_name='allenai/scibert_scivocab_uncased'):
    model = SentenceTransformer(model_name)
    print("[INFO] SciBERT loaded on CPU")
    return model

def get_embedding(model, text):
    return model.encode(text, convert_to_tensor=True).cpu().numpy()
