import pandas as pd
import numpy as np

def calculate_time_weighted_score(
    df: pd.DataFrame,
    period_col='period', score_col='normalized_score',
    decay_constant=0.1
) -> pd.DataFrame:
    df = df.copy()
    df['time_weight'] = np.exp(-df[period_col] * decay_constant)
    weighted = df.groupby('thread_id').apply(
        lambda g: (g['time_weight'] * g[score_col]).sum() * 100 / g[score_col].sum()
    ).reset_index(name='time_weighted_score')
    return weighted 

def calculate_time_weighted_score_logistic(
    df: pd.DataFrame,
    period_col='period', score_col='normalized_score',
    b=2.4, a=0.1
) -> pd.DataFrame:
    df = df.copy()
    df['time_weight'] = 1/(1+np.exp(df[period_col] - b)/a)
    weighted = df.groupby('thread_id').apply(
        lambda g: (g['time_weight'] * g[score_col]).sum() * 100 / g[score_col].sum()
    ).reset_index(name='time_weighted_score')
    return weighted 
