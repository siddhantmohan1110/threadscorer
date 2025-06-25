import pandas as pd
import numpy as np

def score_threads_data(df: pd.DataFrame, decay_constant) -> pd.DataFrame:

# Load the numeric thread dataset from the saved CSV
    df_loaded = pd.read_csv("threads.csv")

    # Repeat the vectorized score calculation on the loaded DataFrame
    df_loaded['score'] = ((df_loaded['likes']*2) + (df_loaded['replies']*3) + (df_loaded['reposts']*2.5)) * np.exp(-df_loaded['age_minutes']/decay_constant)
    
    return df_loaded

def alternate_score_threads_data(df: pd.DataFrame, decay_constant) -> pd.DataFrame:

# Load the numeric thread dataset from the saved CSV
    df_alternate = df.copy() 

    # Repeat the vectorized score calculation on the loaded DataFrame
    df_alternate['score'] = (np.log2((df_alternate['likes']*2) + 1) + np.log2((df_alternate['replies']*3) + 1) + np.log2((df_alternate['reposts']*2.5) + 1)) * np.exp(-df_alternate['age_minutes']/decay_constant)    
    return df_alternate

if __name__ == "__main__":
# Save updated DataFrame
    df_loaded = pd.read_csv("threads.csv")

    df_scored = score_threads_data(df_loaded, decay_constant=120)
    df_scored = alternate_score_threads_data(df_loaded, decay_constant=120)

    csv_path_scored_from_loaded = "threads_scored.csv"
    csv_path_scored_from_loaded_alternate = "alternate_threads_scored.csv"

    df_scored.to_csv(csv_path_scored_from_loaded, index=False)
    df_scored.to_csv(csv_path_scored_from_loaded_alternate, index=False)

