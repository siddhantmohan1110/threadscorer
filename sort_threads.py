import pandas as pd

# Load scored threads data
df = pd.read_csv("threads_scored.csv")

# Sort by score descending
df_top = df.sort_values(by='score', ascending=False).head(10)

# Save top threads
df_top.to_csv("top_threads.csv", index=False)
