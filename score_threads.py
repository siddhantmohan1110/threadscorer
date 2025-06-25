import pandas as pd
import numpy as np

# Load the numeric thread dataset from the saved CSV
df_loaded = pd.read_csv("threads.csv")

# Repeat the vectorized score calculation on the loaded DataFrame
df_loaded['score'] = (df_loaded['likes']*2) + (df_loaded['replies']*3) + (df_loaded['reposts']*2.5) * np.exp(-df_loaded['age_minutes']/120)

# Save updated DataFrame
csv_path_scored_from_loaded = "threads_scored.csv"
df_loaded.to_csv(csv_path_scored_from_loaded, index=False)
