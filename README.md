# ThreadScorer

We are building a three-stage social media feed ranking engine:

Stage 1 – Engagement & Time Decay Scoring:
Each post is assigned a score based on engagement metrics (likes, comments, dislikes, etc.) combined with a logistic time-decay function that adjusts the score based on how many minutes have passed since the post was published. These scores are normalized and converted into probabilities, which determine the likelihood of each post being selected for the feed.

Stage 2 – Interest Alignment via Categories:
Each post is classified into investment-related categories (e.g., crypto, stocks, ETFs). These categories are compared to each user’s interest profile using cosine similarity, and posts most aligned with the user’s preferences are prioritized.

Stage 3 – Engagement Prediction with Decision Trees:
For the shortlisted posts, a decision tree (or boosted ensemble like XGBoost/LightGBM) predicts the probability of user engagement (click, like, share, etc.) based on:

Post-level features (Stage 1 score, raw engagement stats, category match score).
User-level features (past engagement patterns, category interests, time-of-day activity).
Post-user interaction features (recency, relevance, and behavioral patterns).
The predicted engagement probability is combined with earlier scores to produce the final ranking for each user’s feed. Decision trees are used because they handle non-linear interactions between features, work well with mixed data types, and are easy to interpret or scale using ensemble methods.

# Stage-2

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

