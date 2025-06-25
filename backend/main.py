from fastapi import FastAPI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from transformers import pipeline

load_dotenv()

app = FastAPI()

class SentimentRequest(BaseModel):
  text: str

class SentimentResponse(BaseModel):
  text: str
  sentiment: str
  score: float

sentiment_pipeline = None

@app.on_event("startup")
async def load_models():
  global sentiment_pipeline
  print("Loading sentiment analysis model...")
  try:
    import torch
    if torch.cuda.is_available():
      print("CUDA is available! Using GPU for sentiment analysis.")
      sentiment_pipeline = pipeline("sentiment-analysis", device=0)
    else:
      print("CUDA not available. Using CPU for sentiment analysis.")
      sentiment_pipeline = pipeline("sentiment-analysis", device=-1)
  except ImportError:
    print("PyTorch not installed or CUDA not configured. Using CPU for sentiment analysis.")
    sentiment_pipeline = pipeline("sentiment-analysis", device=-1)

  print("Sentiment analysis model loaded successfully.")
@app.get("/")
async def root():
  return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}

@app.get("/env-test")
async def env_test():
  api_key = os.getenv("API_KEY","Not set")
  return {"API_KEY": api_key}

@app.post("/api/analyze/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
  if sentiment_pipeline is None:
    from fastapi import HTTPException
    raise HTTPException(status_code=503, detail="Sentiment analysis model is not loaded yet.")
  
  result = sentiment_pipeline(request.text)[0]

  return SentimentResponse(
        text=request.text,
        sentiment=result['label'],
        score=result['score']
    )
