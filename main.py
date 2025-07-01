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
from score_normalized import calculate_normalized_trending_post_score
from score_time_weighted import calculate_time_weighted_score
from score_category_topic_asset import calculate_trending_category_score


def run_full_pipeline():
    print("--- Starting Thread Scorer Pipeline ---")

    # ---- PARAMS: Easily adjustable for future admin panel ----
    weights = {
        'w1': 0.35, 'w2': 0.25, 'w3': 0.25, 'w4': 0.10, 'w5': 0.05,
        'a1': 0.8, 'a2': 0.1, 'b1': 0.1, 'b2': 0.3
    }
    decay_constant = 0.1

    # 1. Generate the synthetic data
    print("\n1. Generating synthetic thread data...")
    df_threads = generate_synthetic_thread_data(num_threads_min=100, num_threads_max=500)
    print(f"Generated DataFrame with {len(df_threads)} threads.")

    csv_path_raw_threads = "threads.csv"
    df_threads.to_csv(csv_path_raw_threads, index=False)

    # 2. Calculate normalized trending post score
    print("\n2. Calculating normalized trending post scores...")
    df_normalized = calculate_normalized_trending_post_score(
        df_threads,
        w1=weights['w1'], w2=weights['w2'], w3=weights['w3'], w4=weights['w4'], w5=weights['w5'],
        a1=weights['a1'], a2=weights['a2'], b1=weights['b1'], b2=weights['b2']
    )
    csv_path_normalized = "threads_normalized.csv"
    df_normalized.to_csv(csv_path_normalized, index=False)
    print(f"Normalized scores saved to {csv_path_normalized}")

    # 3. (Optional) Simulate periods for time-weighted score
    df_periods = df_normalized.copy()
    df_periods['period'] = np.random.randint(0, 7, len(df_periods))
    df_time_weighted = calculate_time_weighted_score(
        df_periods,
        period_col='period',
        score_col='normalized_score',
        decay_constant=decay_constant
    )
    csv_path_time_weighted = "threads_time_weighted.csv"
    df_time_weighted.to_csv(csv_path_time_weighted, index=False)
    print(f"Time-weighted scores saved to {csv_path_time_weighted}")

    # 4. (Optional) Simulate categories/topics/assets for demo
    df_periods['category'] = np.random.choice(['catA', 'catB', 'catC'], len(df_periods))
    df_periods['topic'] = np.random.choice(['topicX', 'topicY'], len(df_periods))
    df_periods['asset'] = np.random.choice(['asset1', 'asset2', 'asset3'], len(df_periods))

    df_category = calculate_trending_category_score(df_periods, 'category', 'normalized_score')
    df_topic = calculate_trending_category_score(df_periods, 'topic', 'normalized_score')
    df_asset = calculate_trending_category_score(df_periods, 'asset', 'normalized_score')

    df_category.to_csv("trending_category_scores.csv", index=False)
    df_topic.to_csv("trending_topic_scores.csv", index=False)
    df_asset.to_csv("trending_asset_scores.csv", index=False)
    print("Category/Topic/Asset trending scores saved.")

    # 5. Calculate engagement score
    print("\n5. Calculating engagement scores...")
    df_scored = score_threads_data(df_threads, decay_constant=120)
    print("Engagement scores calculated.")

    # (Optional) Save the full scored DataFrame to CSV if needed by external processes
    csv_path_scored = "threads_scored.csv"
    df_scored.to_csv(csv_path_scored, index=False)
    print(f"Full scored data saved to {csv_path_scored}")

    # 6. Assign users to threads
    print("\n6. Assigning users to threads...")
    # This step uses the df_scored data, as it's the full dataset
    df_with_users = assign_users_to_threads(df_scored, num_unique_users=100)
    print(f"User IDs assigned to {len(df_with_users)} threads. Head of DataFrame with users:")
    print(df_with_users.head())

    # (Optional) Save this DataFrame with users to a new CSV as well
    csv_path_with_users = "threads_with_users.csv"
    df_with_users.to_csv(csv_path_with_users, index=False)
    print(f"Data with user assignments saved to {csv_path_with_users}")

    # 7. Get top 10 threads
    print("\n7. Getting top 10 threads...")
    df_top_10 = get_top_threads(df_scored, top_n=10)
    print("Top 10 threads extracted.")

    # (Optional) Save the top 10 threads to CSV if needed by external processes
    csv_path_top_threads = "top_threads.csv"
    df_top_10.to_csv(csv_path_top_threads, index=False)
    print(f"Top 10 threads saved to {csv_path_top_threads}")

    # 8. Calculate Average Post Score for Each User
    print("\n8. Calculating average post score per user...")
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

    # 9. Generate and save plots
    # This function expects the full scored DataFrame and the top 10 DataFrame
    generate_and_save_plots(df_scored, df_top_10, path_scatter="images/score_vs_age.png", path_bar_plot="images/top10_engagements.png")

        # --- ALTERNATE SCORING PIPELINE (STEP 10) ---
    print("\n--- Running Alternate Scoring Pipeline ---")

    # 10a. Calculate alternate engagement score
    print("\n10a. Calculating ALTERNATE engagement scores...")
    df_scored_alternate = alternate_score_threads_data(df_threads, decay_constant=120)
    print("Alternate engagement scores calculated.")

    # Save the full scored DataFrame (Alternate)
    csv_path_scored_alternate = "threads_scored_alternate.csv"
    df_scored_alternate.to_csv(csv_path_scored_alternate, index=False)
    print(f"Full ALTERNATE scored data saved to {csv_path_scored_alternate}")

    # 10b. Assign users to threads (Alternate Scored Data)
    print("\n10b. Assigning users to ALTERNATE scored threads...")
    df_with_users_alternate = assign_users_to_threads(df_scored_alternate, num_unique_users=100)
    print(f"User IDs assigned to {len(df_with_users_alternate)} ALTERNATE scored threads.")

    csv_path_with_users_alternate = "threads_with_users_alternate.csv"
    df_with_users_alternate.to_csv(csv_path_with_users_alternate, index=False)
    print(f"ALTERNATE data with user assignments saved to {csv_path_with_users_alternate}")

    # 10c. Get top 10 threads (Alternate Scored Data)
    print("\n10c. Getting top 10 ALTERNATE scored threads...")
    # IMPORTANT: get_top_threads needs to be flexible for 'alternate_score'
    df_top_10_alternate = get_top_threads(df_scored_alternate, top_n=10)
    print("Top 10 ALTERNATE threads extracted.")

    csv_path_top_threads_alternate = "top_threads_alternate.csv"
    df_top_10_alternate.to_csv(csv_path_top_threads_alternate, index=False)
    print(f"Top 10 ALTERNATE threads saved to {csv_path_top_threads_alternate}")

    # 10d. Calculate Average Post Score for Each User (Alternate Scored Data)
    print("\n10d. Calculating average post score per user for ALTERNATE data...")
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

    # 10e. Generate and save plots (Alternate Scored Data)
    print("\n10e. Generating plots for ALTERNATE scored data...")
    # IMPORTANT: generate_and_save_plots needs to be flexible for 'alternate_score' and plot prefix
    generate_and_save_plots(df_scored_alternate, df_top_10_alternate, path_scatter="images/alter_score_vs_age.png", path_bar_plot="images/alter_top10_engagements.png")
    print("All ALTERNATE plots generated and saved.")

    print("\n--- Thread Scorer Pipeline Completed ---")

if __name__ == "__main__":
    run_full_pipeline()