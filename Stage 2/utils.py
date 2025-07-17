# utils.py

import os
import json
import hashlib
from dotenv import load_dotenv

print("📦 Importing cosine_similarity...")
from sklearn.metrics.pairwise import cosine_similarity

print("📦 Importing OpenAI...")
from openai import OpenAI

# Load API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Constants
EMBEDDING_MODEL = "text-embedding-3-small"
CACHE_DIR = ".embedding_cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def hash_text(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def cache_embedding(text):
    h = hash_text(text)
    path = os.path.join(CACHE_DIR, f"{h}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=[text])
        emb = response.data[0].embedding
        with open(path, "w", encoding="utf-8") as f:
            json.dump(emb, f)
        return emb


def compute_similarity(embedding_a, embedding_b):
    return cosine_similarity([embedding_a], [embedding_b])[0][0]


def clear_cache():
    print(f"🧹 Clearing cache directory: {CACHE_DIR}")
    count = 0
    for file in os.listdir(CACHE_DIR):
        if file.endswith(".json"):
            os.remove(os.path.join(CACHE_DIR, file))
            count += 1
    print(f"✅ Removed {count} cached files.")

