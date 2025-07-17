# post.py

from typing import Optional

class Post:
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.topics_vector: Optional[list[tuple[str, float]]] = None

    def classify(self, centroid_path="topic_centroids.json", top_n=13):
        """Classify this post and save the similarity vector."""
        from embeddings import classify_post_against_topics
        self.topics_vector = classify_post_against_topics(self, centroid_path, top_n)
        return self.topics_vector

    def full_text(self):
        """Concatenate title and text for embedding or classification."""
        return f"{self.title}\n\n{self.text}"

    def preview(self, max_chars=120):
        """Return a shortened preview for logs or summaries."""
        content = self.full_text().replace("\n", " ")
        return (content[:max_chars] + "…") if len(content) > max_chars else content

    def __repr__(self):
        return f"Post(title={self.title!r}, text={self.text[:40]!r}...)"
