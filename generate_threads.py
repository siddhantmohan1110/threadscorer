import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# Choose a random number of threads between 100 and 500
num_threads = random.randint(100, 500)

# Generate synthetic data
data = {
    'thread_id': list(range(1, num_threads + 1)),
    'likes': np.random.randint(0, 101, num_threads),
    'replies': np.random.randint(0, 51, num_threads),
    'reposts': np.random.randint(0, 31, num_threads),
    'age_minutes': np.random.randint(0, 361, num_threads)
}

# Create a DataFrame
df_threads = pd.DataFrame(data)

# Save to CSV
csv_path = "threads.csv"
df_threads.to_csv(csv_path, index=False)