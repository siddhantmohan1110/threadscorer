import pandas as pd
import numpy as np
import random

# Import functions from your other modules
from generate_threads import generate_synthetic_thread_data
from score_threads import score_threads_data
from sort_threads import get_top_threads
from multi_user import assign_users_to_threads
from plot_threads import generate_and_save_plots
from plot_threads import generate_and_save_plots
from multi_user_analysis import calculate_average_score_per_user, plot_user_performance_distribution # <--- UPDATED IMPORT


def run_full_pipeline():
    print("--- Starting Thread Scorer Pipeline ---")

    # 1. Generate the synthetic data
    print("\n1. Generating synthetic thread data...")
    # generate_synthetic_thread_data already contains its own seeding.
    df_threads = generate_synthetic_thread_data(num_threads_min=100, num_threads_max=500)
    print(f"Generated DataFrame with {len(df_threads)} threads.")

    csv_path_raw_threads = "threads.csv"
    df_threads.to_csv(csv_path_raw_threads, index=False)

    # 2. Calculate engagement score
    print("\n2. Calculating engagement scores...")
    df_scored = score_threads_data(df_threads, decay_constant=120)
    print("Engagement scores calculated.")

    # (Optional) Save the full scored DataFrame to CSV if needed by external processes
    csv_path_scored = "threads_scored.csv"
    df_scored.to_csv(csv_path_scored, index=False)
    print(f"Full scored data saved to {csv_path_scored}")

    # 3. Assign users to threads
    print("\n3. Assigning users to threads...")
    # This step uses the df_scored data, as it's the full dataset
    df_with_users = assign_users_to_threads(df_scored, num_unique_users=100)
    print(f"User IDs assigned to {len(df_with_users)} threads. Head of DataFrame with users:")
    print(df_with_users.head())

    # (Optional) Save this DataFrame with users to a new CSV as well
    csv_path_with_users = "threads_with_users.csv"
    df_with_users.to_csv(csv_path_with_users, index=False)
    print(f"Data with user assignments saved to {csv_path_with_users}")

    # 4. Get top 10 threads
    print("\n4. Getting top 10 threads...")
    df_top_10 = get_top_threads(df_scored, top_n=10)
    print("Top 10 threads extracted.")

    # (Optional) Save the top 10 threads to CSV if needed by external processes
    csv_path_top_threads = "top_threads.csv"
    df_top_10.to_csv(csv_path_top_threads, index=False)
    print(f"Top 10 threads saved to {csv_path_top_threads}")

    # 5. Calculate Average Post Score for Each User
    print("\n5. Calculating average post score per user...")
    df_user_avg_scores = calculate_average_score_per_user(input_csv_path=csv_path_with_users)
    if not df_user_avg_scores.empty:
        print("Average post score per user calculated. Head:")
        print(df_user_avg_scores.head())
        print(f"Total unique users with scores: {len(df_user_avg_scores)}")

        # Save the user average scores to a CSV
        output_csv_path_avg_scores = "user_average_scores.csv"
        df_user_avg_scores.to_csv(output_csv_path_avg_scores, index=False)
        print(f"User average scores saved to {output_csv_path_avg_scores}")

        # Plot user performance distribution
        print("\nPlotting user performance distribution...")
        plot_user_performance_distribution(df_user_avg_scores)
    else:
        print("Could not calculate user average scores or plot distribution.")

    # 6. Generate and save plots
    # This function expects the full scored DataFrame and the top 10 DataFrame
    generate_and_save_plots(df_scored, df_top_10)
    

    print("\n--- Thread Scorer Pipeline Completed ---")

if __name__ == "__main__":
    run_full_pipeline()