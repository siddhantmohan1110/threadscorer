# user.py

from typing import Dict
from post import Post

class User:
    def __init__(self, name: str, interact_alpha: float = 0.1, engage_alpha: float = 0.05):
        self.name = name
        # EMA alpha factors (0 < alpha < 1). Higher = more weight on new post.
        self.interact_alpha = interact_alpha
        self.engage_alpha = engage_alpha
        self.topic_vector: Dict[str, float] = {}

    def interact(self, post: Post):
        """
        User interacts (e.g., likes or shares). Higher weight than engagement.
        """
        if post.topics_vector is None:
            raise ValueError("Post must be classified before interaction.")

        print(f"👤 {self.name} interacted with {post.title}")
        self.update_topic_vector(post_scores=post.topics_vector, alpha=self.interact_alpha)

    def engage(self, post: Post):
        """
        User engages (e.g., views for 5+ seconds). Lower influence on profile.
        """
        if post.topics_vector is None:
            raise ValueError("Post must be classified before engagement.")

        print(f"👤 {self.name} engaged with {post.title}")
        self.update_topic_vector(post_scores=post.topics_vector, alpha=self.engage_alpha)

    def update_topic_vector(self, post_scores: list[tuple[str, float]], alpha: float, top_n: int = 5):
        """
        Applies EMA update to user's topic_vector using the given alpha,
        only for the top-N topics with highest similarity scores.
        """
        top_scores = sorted(post_scores, key=lambda x: x[1], reverse=True)[:top_n]

        for topic, score in top_scores:
            if topic in self.topic_vector:
                self.topic_vector[topic] = (1 - alpha) * self.topic_vector[topic] + alpha * score
            else:
                self.topic_vector[topic] = score

    def get_sorted_topics(self, top_n=13):
        """
        Returns top-N topics by interest level.
        """
        return sorted(self.topic_vector.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def __repr__(self):
        return f"User(name={self.name!r}, topics={len(self.topic_vector)} tracked)"

