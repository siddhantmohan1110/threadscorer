import pandas as pd
import matplotlib.pyplot as plt

# Load full scored dataset
df = pd.read_csv("threads_scored.csv")

# Load top 10 threads dataset
df_top10 = pd.read_csv("top_threads.csv")

# --- Plot 1: Score vs. Age of Thread ---
plt.figure(figsize=(8, 6))
plt.scatter(df['age_minutes'], df['score'], alpha=0.7)
plt.xlabel('Age (minutes)')
plt.ylabel('Score')
plt.title('Score vs. Age of Thread')
plt.grid(True)
plt.tight_layout()
plt.savefig("images/score_vs_age.png")

# --- Plot 2: Distribution of engagement types across top 10 threads ---
engagement_top10 = df_top10[['thread_id', 'likes', 'replies', 'reposts']].set_index('thread_id')

engagement_top10.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Thread ID')
plt.ylabel('Count')
plt.title('Distribution of Engagement Types Across Top 10 Threads')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/top10_engagements.png")