import pandas as pd

def calculate_normalized_trending_post_score(
    df: pd.DataFrame,
    w1=0.35, w2=0.25, w3=0.25, w4=0.10, w5=0.05,
    a1=0.8, a2=0.1, b1=0.1, b2=0.3
) -> pd.DataFrame:
    df = df.copy()
    T = (
        df['reposts'] + df['other_interactions'] + df['replies'] +
        (a1 * df['likes'] + a2 * df['dislikes']) +
        (b1 * df['cursory_views'] + b2 * df['engaged_views'])
    )
    score = (
        w1 * df['reposts'] +
        w2 * df['other_interactions'] +
        w3 * df['replies'] +
        w4 * (a1 * df['likes'] + a2 * df['dislikes']) +
        w5 * (b1 * df['cursory_views'] + b2 * df['engaged_views'])
    ) * (100 / T)
    df['normalized_score'] = score
    return df 