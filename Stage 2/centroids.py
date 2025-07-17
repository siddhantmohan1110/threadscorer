# centroids.py

import json
import numpy as np
from utils import cache_embedding, clear_cache
from topics import TOPIC_EXAMPLES

CENTROID_FILE = "topic_centroids.json"

def average_embeddings(texts):
    vectors = [cache_embedding(t) for t in texts]
    return list(np.mean(vectors, axis=0))

def create_centroid_embeddings():
    print("🧠 Generating topic centroid embeddings from example posts...")
    centroids = {}
    for topic, examples in TOPIC_EXAMPLES.items():
        print(f"🔹 Embedding topic: {topic} ({len(examples)} examples)")
        centroids[topic] = average_embeddings(examples)
    return centroids

def save_centroids(centroids, path=CENTROID_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(centroids, f)
    print(f"✅ Saved centroid embeddings to {path}")

if __name__ == "__main__":
    centroids = create_centroid_embeddings()
    save_centroids(centroids)
