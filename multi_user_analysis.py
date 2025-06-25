import uuid
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_average_score_per_user(input_csv_path: str = "threads_with_users.csv") -> pd.DataFrame:
    #calculate average score for each user
    df = pd.read_csv(input_csv_path)
    average_scores_df = df.groupby('user_id')['score'].mean().reset_index()

    return average_scores_df



def plot_user_performance_distribution(df_user_scores: pd.DataFrame, plot_path: str):


    #generate plot for each user
    plt.figure(figsize=(10, 6))
    plt.hist(df_user_scores['score'], bins=20, edgecolor='black', alpha=0.7)
    plt.xlabel('Average Post Score')
    plt.ylabel('Number of Users')
    plt.title('Distribution of Average Post Scores Per User')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()

    plt.savefig(plot_path)
    plt.close() # Close the figure to free up memory


if __name__ == "__main__":
    print("Running analyze_users.py directly.")
    avg_scores = calculate_average_score_per_user()
    if not avg_scores.empty:
        print("\nAverage scores per user (direct run):")
        print(avg_scores.head())
        print(f"Total unique users found: {len(avg_scores)}")

        output_csv_path = "user_average_scores.csv"
        avg_scores.to_csv(output_csv_path, index=False)
        print(f"Average scores saved to {output_csv_path}")

        # Plot the distribution when run directly
        plot_user_performance_distribution(avg_scores)
        print("User performance distribution plot generated (direct run).")
