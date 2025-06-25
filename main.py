import pandas as pd
import numpy as np
import random

# Import functions from your other modules
from generate_threads import generate_synthetic_thread_data
from score_threads import score_threads_data
from score_threads import alternate_score_threads_data
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
        plot_user_performance_distribution(df_user_avg_scores, plot_path="images/user_score_distribution.png")
    else:
        print("Could not calculate user average scores or plot distribution.")

    # 6. Generate and save plots
    # This function expects the full scored DataFrame and the top 10 DataFrame
    generate_and_save_plots(df_scored, df_top_10, path_scatter="images/score_vs_age.png", path_bar_plot="images/top10_engagements.png")

        # --- ALTERNATE SCORING PIPELINE (STEP 7) ---
    print("\n--- Running Alternate Scoring Pipeline ---")

    # 7a. Calculate alternate engagement score
    print("\n7a. Calculating ALTERNATE engagement scores...")
    df_scored_alternate = alternate_score_threads_data(df_threads, decay_constant=120)
    print("Alternate engagement scores calculated.")

    # Save the full scored DataFrame (Alternate)
    csv_path_scored_alternate = "threads_scored_alternate.csv"
    df_scored_alternate.to_csv(csv_path_scored_alternate, index=False)
    print(f"Full ALTERNATE scored data saved to {csv_path_scored_alternate}")

    # 7b. Assign users to threads (Alternate Scored Data)
    print("\n7b. Assigning users to ALTERNATE scored threads...")
    df_with_users_alternate = assign_users_to_threads(df_scored_alternate, num_unique_users=100)
    print(f"User IDs assigned to {len(df_with_users_alternate)} ALTERNATE scored threads.")

    csv_path_with_users_alternate = "threads_with_users_alternate.csv"
    df_with_users_alternate.to_csv(csv_path_with_users_alternate, index=False)
    print(f"ALTERNATE data with user assignments saved to {csv_path_with_users_alternate}")

    # 7c. Get top 10 threads (Alternate Scored Data)
    print("\n7c. Getting top 10 ALTERNATE scored threads...")
    # IMPORTANT: get_top_threads needs to be flexible for 'alternate_score'
    df_top_10_alternate = get_top_threads(df_scored_alternate, top_n=10)
    print("Top 10 ALTERNATE threads extracted.")

    csv_path_top_threads_alternate = "top_threads_alternate.csv"
    df_top_10_alternate.to_csv(csv_path_top_threads_alternate, index=False)
    print(f"Top 10 ALTERNATE threads saved to {csv_path_top_threads_alternate}")

    # 7d. Calculate Average Post Score for Each User (Alternate Scored Data)
    print("\n7d. Calculating average post score per user for ALTERNATE data...")
    # IMPORTANT: calculate_average_score_per_user needs to be flexible for 'alternate_score'
    df_user_avg_scores_alternate = calculate_average_score_per_user(csv_path_with_users_alternate)
    
    if not df_user_avg_scores_alternate.empty:
        print("Average post score per user calculated for ALTERNATE data. Head:")
        print(df_user_avg_scores_alternate.head())
        print(f"Total unique users with scores (ALTERNATE): {len(df_user_avg_scores_alternate)}")

        csv_path_avg_scores_alternate = "user_average_scores_alternate.csv"
        df_user_avg_scores_alternate.to_csv(csv_path_avg_scores_alternate, index=False)
        print(f"ALTERNATE User average scores saved to {csv_path_avg_scores_alternate}")

        print("\nPlotting ALTERNATE user performance distribution...")
        plot_user_performance_distribution(df_user_avg_scores_alternate, plot_path="images/alter_user_score_distribution.png")
    else:
        print("Could not calculate user average scores or plot distribution for ALTERNATE data.")

    # 7e. Generate and save plots (Alternate Scored Data)
    print("\n7e. Generating plots for ALTERNATE scored data...")
    # IMPORTANT: generate_and_save_plots needs to be flexible for 'alternate_score' and plot prefix
    generate_and_save_plots(df_scored_alternate, df_top_10_alternate, path_scatter="images/alter_score_vs_age.png", path_bar_plot="images/alter_top10_engagements.png")
    print("All ALTERNATE plots generated and saved.")

    print("\n--- Thread Scorer Pipeline Completed ---")

if __name__ == "__main__":
    run_full_pipeline()