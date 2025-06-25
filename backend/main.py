from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

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