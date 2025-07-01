import pandas as pd

def calculate_trending_category_score(df: pd.DataFrame, group_col: str, score_col: str) -> pd.DataFrame:
    grouped = df.groupby(group_col)[score_col].mean().reset_index()
    grouped = grouped.rename(columns={score_col: f'trending_{group_col}_score'})
    return grouped 