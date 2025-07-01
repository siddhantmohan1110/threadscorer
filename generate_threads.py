import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
SEED = 42

def generate_synthetic_thread_data(num_threads_min=100, num_threads_max=500):
# Choose a random number of threads between 100 and 500
    np.random.seed(SEED)
    random.seed(SEED)
    num_threads = random.randint(num_threads_min, num_threads_max)

    # Generate synthetic data
    data = {
        'thread_id': list(range(1, num_threads + 1)),
        'likes': np.random.randint(0, 101, num_threads),
        'dislikes': np.random.randint(0, 51, num_threads),
        'replies': np.random.randint(0, 51, num_threads),
        'reposts': np.random.randint(0, 31, num_threads),
        'other_interactions': np.random.randint(0, 51, num_threads),
        'cursory_views': np.random.randint(0, 201, num_threads),
        'engaged_views': np.random.randint(0, 101, num_threads),
        'age_minutes': np.random.randint(0, 361, num_threads)
    }

    # Create a DataFrame
    df_threads = pd.DataFrame(data)
    return df_threads

# Save to CSV
if __name__ == "__main__":
    df_generated = generate_synthetic_thread_data()
    csv_path = "threads.csv"
    df_generated.to_csv(csv_path, index=False)