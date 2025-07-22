# ThreadScorer

**ThreadScorer** is a topic classification and user interest profiling system designed for social media feeds, with a focus on investment and finance discussions.  
It uses OpenAI’s `text-embedding-3-small` model to embed posts, classifies them against predefined topic centroids, and builds dynamic user profiles based on interactions.

---

## Features

- **Topic Classification**  
  Classifies posts into 13 predefined financial/investing topics using centroid-based embeddings.

- **Post Similarity Scoring**  
  Compares posts by cosine similarity of their embeddings.

- **User Interest Profiling**  
  Tracks user interests via an **Exponential Moving Average (EMA)** update based on interactions (likes, shares, views).

- **Caching for Efficiency**  
  Caches embeddings locally to avoid redundant API calls.

---

## Topics

ThreadScorer classifies posts into these topics:
- Stocks  
- Crypto  
- Real Estate  
- Economy  
- Tech Sector  
- Energy Sector  
- Portfolio Strategy  
- Trading Tips  
- Long-Term Investing  
- Market News  
- Speculation  
- Sentiment (Bullish / Bearish)

Each topic is seeded with example posts (`topics.py`) used to generate **centroid embeddings**.

---

## Project Structure

threadscorer/
│
├── centroids.py          # Builds topic centroid embeddings
├── embeddings.py         # Classifies posts and compares similarity
├── post.py               # Defines Post class (title, text, classification)
├── user.py               # Defines User class for topic interest tracking
├── utils.py              # Embedding + cosine similarity + cache handling
├── topics.py             # Predefined topic categories and example posts
├── test_posts.py         # Sample Post objects for testing
└── topic_centroids.json  # Generated centroid embeddings (created by centroids.py)

