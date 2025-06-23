import pandas as pd
import numpy as np

# Load the numeric thread dataset from the saved CSV
df_loaded = pd.read_csv("threads.csv")

# Repeat the vectorized score calculation on the loaded DataFrame

# Extract columns as arrays
likes = df_loaded['likes'].to_numpy()
replies = df_loaded['replies'].to_numpy()
reposts = df_loaded['reposts'].to_numpy()
age_minutes = df_loaded['age_minutes'].to_numpy()

# Compute decay
age_decay = np.exp(-age_minutes / 120)

# Compute score parts
likes_part = likes * 2
replies_part = replies * 3
reposts_part = reposts * 2.5 * age_decay

# Compute final score
score = likes_part + replies_part + reposts_part

# Append score to DataFrame
df_loaded['score'] = score

# Save updated DataFrame
csv_path_scored_from_loaded = "threads_scored.csv"
df_loaded.to_csv(csv_path_scored_from_loaded, index=False)
