import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description="Sample script")

# Add arguments
parser.add_argument('--formula', type=int, default=1, help='Score formula 1 or 2')

# Parse arguments
args = parser.parse_args()

# Load the numeric thread dataset from the saved CSV
df_loaded = pd.read_csv("threads.csv")

# Vectorized score calculation - formula 1
if args.formula==1:
    df_loaded['score'] = (df_loaded['likes']*2) + (df_loaded['replies']*3) + (df_loaded['reposts']*2.5) * np.exp(-df_loaded['age_minutes']/120)
elif args.formula==2:
    # Vectorized score calculation - formula 2
    df_loaded['score'] = ((df_loaded['likes']*2) + (df_loaded['replies']*3) + (df_loaded['reposts']*2.5)) * np.exp(-df_loaded['age_minutes']/120)
else:
    print("Invalid formula!")

if args.formula==1 or args.formula==2:
    # Save updated DataFrame
    csv_path_scored_from_loaded = "threads_scored.csv"
    df_loaded.to_csv(csv_path_scored_from_loaded, index=False)