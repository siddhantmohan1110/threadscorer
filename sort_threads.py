import pandas as pd

def get_top_threads(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:

    # Sort by score descending
    df_top = df.sort_values(by='score', ascending=False).head(top_n)
    return df_top

if __name__ == "__main__":
# Save top threads
    
    df = pd.read_csv("threads_scored.csv") # Load scored threads data
    df_top = get_top_threads(df)
    csv_path_top_threads = "top_threads.csv" # Save top threads
    df_top.to_csv(csv_path_top_threads, index=False)
