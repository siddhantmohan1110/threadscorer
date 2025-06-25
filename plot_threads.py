import pandas as pd
import matplotlib.pyplot as plt

def generate_and_save_plots(df_full_scored: pd.DataFrame, df_top_10: pd.DataFrame, path_scatter: str, path_bar_plot:str):

    # --- Plot 1: Score vs. Age of Thread ---
    plt.figure(figsize=(8, 6))
    plt.scatter(df_full_scored['age_minutes'], df_full_scored['score'], alpha=0.7)
    plt.xlabel('Age (minutes)')
    plt.ylabel('Score')
    plt.title('Score vs. Age of Thread')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path_scatter)
    plt.close() # Close the figure to free up memory

    # --- Plot 2: Distribution of engagement types across top 10 threads ---
    engagement_top10 = df_top_10[['thread_id', 'likes', 'replies', 'reposts']].set_index('thread_id')

    engagement_top10.plot(kind='bar', figsize=(10, 6))
    plt.xlabel('Thread ID')
    plt.ylabel('Count')
    plt.title('Distribution of Engagement Types Across Top 10 Threads')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path_bar_plot)
    plt.close() # Close the figure

if __name__ == "__main__":    
    df = pd.read_csv("threads_scored.csv") # Load full scored dataset
    df_top10 = pd.read_csv("top_threads.csv") # Load top 10 threads dataset
    generate_and_save_plots(df, df_top10)

