# src/api/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from pipeline.inference import run_inference

app = FastAPI()

class TextInput(BaseModel):
    texts: list

@app.post("/embed/")
def embed_text(input_data: TextInput):
    embeddings = run_inference(input_data.texts)
    return {"embeddings": [e.tolist() for e in embeddings]}
