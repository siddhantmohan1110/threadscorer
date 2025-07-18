import pandas as pd
import numpy as np
from score_time_weighted import calculate_time_weighted_score, calculate_time_weighted_score_logistic

def normalize_scores_to_probabilities(scores_df: pd.DataFrame, score_col='time_weighted_score') -> pd.DataFrame:
    df = scores_df.copy()
    
    # Apply sigmoid function to transform scores to (0, 1) range
    # Using sigmoid: 1 / (1 + exp(-x))
    sigmoid_scores = 1 / (1 + np.exp(-df[score_col]))
    
    # Normalize sigmoid scores to probabilities that sum to 1
    total_sigmoid = sigmoid_scores.sum()
    if total_sigmoid > 0:
        df['probability'] = sigmoid_scores / total_sigmoid
    else:
        # If all sigmoid scores are 0 (shouldn't happen with sigmoid), assign equal probability
        df['probability'] = 1.0 / len(df)
    
    return df

def sample_threads_by_probability(
    scores_df: pd.DataFrame, 
    n_samples=10, 
    score_col='time_weighted_score',
    replace=True,
    random_seed=None
) -> pd.DataFrame:
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Normalize scores to probabilities
    df_probs = normalize_scores_to_probabilities(scores_df, score_col)
    
    # Sample threads based on probabilities
    sampled_indices = np.random.choice(
        len(df_probs),
        size=min(n_samples, len(df_probs)) if not replace else n_samples,
        replace=replace,
        p=df_probs['probability'].values
    )
    
    # Get sampled threads
    sampled_threads = df_probs.iloc[sampled_indices].copy()
    sampled_threads['sample_order'] = range(len(sampled_threads))
    
    return sampled_threads[['thread_id', 'probability', 'sample_order']].reset_index(drop=True)

def recommend_threads_exponential(
    df: pd.DataFrame,
    n_recommendations=5,
    period_col='period',
    score_col='normalized_score',
    decay_constant=0.1,
    random_seed=None
) -> pd.DataFrame:
    # Calculate time-weighted scores
    weighted_scores = calculate_time_weighted_score(
        df, period_col, score_col, decay_constant
    )
    # Sample recommended threads
    recommendations = sample_threads_by_probability(
        weighted_scores,
        n_samples=n_recommendations,
        random_seed=random_seed
    )
    
    return recommendations

def recommend_threads_logistic(
    df: pd.DataFrame,
    n_recommendations=5,
    period_col='period',
    score_col='normalized_score',
    inflection=120,
    steepness=20,
    random_seed=None
) -> pd.DataFrame:
    """
    Complete pipeline: calculate time-weighted scores using logistic function,
    normalize to probabilities, and sample recommended threads.
    
    Args:
        df: Input DataFrame with thread data
        n_recommendations: Number of threads to recommend
        period_col: Column name for time period
        score_col: Column name for base scores
        inflection: Logistic function inflection point (formerly b)
        steepness: Logistic function steepness parameter (formerly a)
        random_seed: Random seed for reproducibility
    
    Returns:
        DataFrame with recommended thread_ids and their selection probabilities
    """
    # Calculate time-weighted scores
    weighted_scores = calculate_time_weighted_score_logistic(
        df, period_col, score_col, inflection, steepness
    )
    
    # Sample recommended threads
    recommendations = sample_threads_by_probability(
        weighted_scores,
        n_samples=n_recommendations,
        random_seed=random_seed
    )
    
    return recommendations



