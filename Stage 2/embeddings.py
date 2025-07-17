# embeddings.py

import json
from utils import cache_embedding, compute_similarity, clear_cache
from post import Post

def compare_posts(post_a: Post, post_b: Post):
    print("\n\n🆚 Comparing Posts A and B...")

    print("🧠 Embedding Post A...")
    emb_a = cache_embedding(post_a.full_text())

    print("🧠 Embedding Post B...")
    emb_b = cache_embedding(post_b.full_text())

    similarity = compute_similarity(emb_a, emb_b)
    print(f"🔍 Similarity score: {similarity:.4f}")

    if similarity > 0.7:
        print("✅ Posts are very similar.")
    elif similarity > 0.4:
        print("🟡 Posts are moderately similar.")
    else:
        print("❌ Posts are not very similar.")


def classify_post_against_topics(post: Post, centroid_path="topic_centroids.json", top_n=13):
    print("🧠 Embedding post to classify...")
    post_emb = cache_embedding(post.full_text())

    print(f"📂 Loading topic centroids from {centroid_path}...")
    with open(centroid_path, "r", encoding="utf-8") as f:
        topic_centroids = json.load(f)

    print("🔎 Comparing to topic centroids...")
    similarities = {
        topic: compute_similarity(post_emb, centroid)
        for topic, centroid in topic_centroids.items()
    }

    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    print("\n📌 Top topic matches:")
    for topic, score in sorted_similarities[:top_n]:
        print(f"   {topic:20s} {score:.4f}")

    return sorted_similarities


if __name__ == "__main__":
    import random
    from test_posts import get_test_posts
    from user import User

    clear_cache()

    # ✅ Similar investing posts
    post1 = Post(
        title="Tesla Earnings Watch",
        text="Thinking of shorting Tesla ahead of earnings — RSI and volume both look bearish."
    )
    post2 = Post(
        title="Bearish on Tesla Before Report",
        text="If Tesla disappoints on earnings, we could see a big selloff. Technicals look weak to me."
    )
    compare_posts(post1, post2)

    # ❌ Dissimilar posts
    post3 = Post(
        title="Ethereum ETF Approval",
        text="Big win for crypto today — the SEC just approved a spot Ethereum ETF. Bullish for the entire market."
    )
    post4 = Post(
        title="Rising Mortgage Rates",
        text="Interest rates just jumped again. Housing affordability is getting crushed this year."
    )
    compare_posts(post3, post4)

    # ➕ Classification examples
    print("\n\n🪣 Classifying Tesla post:")
    investing_post = Post(
        title="Tesla Earnings Play",
        text="Thinking of shorting Tesla before earnings — this chart looks weak 📉"
    )
    investing_post.classify()

    print("\n\n🪣 Classifying ETH post:")
    crypto_post = Post(
        title="Ethereum ETF Approval",
        text="Big win for crypto today — the SEC just approved a spot Ethereum ETF. Bullish for the entire market."
    )
    crypto_post.classify()

    print("\n\n🪣 Classifying housing post:")
    real_estate_post = Post(
        title="Rising Mortgage Rates",
        text="Interest rates just jumped again. Housing affordability is getting crushed this year."
    )
    real_estate_post.classify()

    print("\n\n")

    # Simulate user interactions
    user = User("Chris")

    chris_interests = {"crypto", "tech_sector", "energy_sector"}  # Topics Chris is more likely to engage with

    test_posts = get_test_posts()
    for post in test_posts:
        post.classify()

        # Determine if post matches any of Chris's interests (using top-5 topics)
        top_topics = sorted(post.topics_vector, key=lambda x: x[1], reverse=True)[:5]
        top_topic_names = [topic for topic, _ in top_topics]
        is_interested = any(topic in chris_interests for topic in top_topic_names)

        # Boost probabilities if interested
        rand = random.random()
        if is_interested:
            if rand < 0.7:
                user.interact(post)  # 70% interact
            elif rand < 0.9:
                user.engage(post)    # 20% engage
            else:
                pass                 # 10% ignore
        else:
            if rand < 0.1:
                user.interact(post)  # 10% interact
            elif rand < 0.4:
                user.engage(post)    # 30% engage
            else:
                pass                 # 50% ignore

        print("\n\n")


    print("\n📊 Final user topic profile:")
    for topic, score in user.get_sorted_topics():
        print(f"   {topic:20s} {score:.4f}")

    print("\n\n")

