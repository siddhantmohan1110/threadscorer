from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np

from generate_threads import generate_synthetic_thread_data
from score_normalized import calculate_normalized_trending_post_score
from score_time_weighted import calculate_time_weighted_score
from score_threads import score_threads_data, alternate_score_threads_data
from score_probability import recommend_threads_exponential, recommend_threads_logistic

# --- App setup ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo, allow all. Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Generate data ONCE with fixed seed ---
THREADS_DF = generate_synthetic_thread_data(num_threads_min=100, num_threads_max=100)

# --- Pydantic model for weights ---
class Weights(BaseModel):
    w1: float = 0.35
    w2: float = 0.25
    w3: float = 0.25
    w4: float = 0.10
    w5: float = 0.05
    a1: float = 0.8
    a2: float = 0.1
    b1: float = 0.1
    b2: float = 0.3
    decay_constant: float = 0.1

class RecommendationRequest(BaseModel):
    w1: float = 0.35
    w2: float = 0.25
    w3: float = 0.25
    w4: float = 0.10
    w5: float = 0.05
    a1: float = 0.8
    a2: float = 0.1
    b1: float = 0.1
    b2: float = 0.3
    decay_constant: float = 0.1
    inflection: float = 120.0
    steepness: float = 20.0
    n_recommendations: int = 10
    random_seed: int = 42
    use_logistic: bool = False

@app.get("/")
def root():
    return {"message": "Thread Score Demo API"}

@app.post("/scores")
def get_scores(weights: Weights):
    df = THREADS_DF.copy()

    # Calculate original score using the modular function
    df_score = score_threads_data(df, decay_constant=120)
    df['score'] = df_score['score']

    # Calculate alternate score using the modular function
    df_alt = alternate_score_threads_data(df, decay_constant=120)
    df['alternate_score'] = df_alt['score']

    # Normalized trending post score
    df_norm = calculate_normalized_trending_post_score(
        df,
        w1=weights.w1, w2=weights.w2, w3=weights.w3, w4=weights.w4, w5=weights.w5,
        a1=weights.a1, a2=weights.a2, b1=weights.b1, b2=weights.b2
    )
    df['normalized_score'] = df_norm['normalized_score']

    # Simulate periods for time-weighted score
    df['period'] = np.random.randint(0, 7, len(df))
    df_time_weighted = calculate_time_weighted_score(
        df,
        period_col='period',
        score_col='normalized_score',
        decay_constant=weights.decay_constant
    )
    df = df.merge(df_time_weighted, on='thread_id', how='left')

    # Return as JSON
    return {
        "columns": [
            "thread_id", "likes", "dislikes", "replies", "reposts", "other_interactions",
            "cursory_views", "engaged_views", "age_minutes",
            "score", "alternate_score", "normalized_score", "time_weighted_score"
        ],
        "data": [
            {
                "thread_id": int(row.thread_id),
                "likes": int(row.likes),
                "dislikes": int(row.dislikes),
                "replies": int(row.replies),
                "reposts": int(row.reposts),
                "other_interactions": int(row.other_interactions),
                "cursory_views": int(row.cursory_views),
                "engaged_views": int(row.engaged_views),
                "age_minutes": int(row.age_minutes),
                "score": float(row.score),
                "alternate_score": float(row.alternate_score),
                "normalized_score": float(row.normalized_score),
                "time_weighted_score": float(row.time_weighted_score),
            }
            for _, row in df.iterrows()
        ]
    }

@app.post("/recommendations")
def get_recommendations(request: RecommendationRequest):
    """
    Get probability-based thread recommendations using sigmoid normalization
    """
    df = THREADS_DF.copy()
    
    # Calculate normalized trending post score
    df_norm = calculate_normalized_trending_post_score(
        df,
        w1=request.w1, w2=request.w2, w3=request.w3, w4=request.w4, w5=request.w5,
        a1=request.a1, a2=request.a2, b1=request.b1, b2=request.b2
    )
    df['normalized_score'] = df_norm['normalized_score']
    
    # Simulate periods for time-weighted score
    df['period'] = np.random.randint(0, 7, len(df))
    
    # Get probability-based recommendations
    if request.use_logistic:
        recommendations = recommend_threads_logistic(
            df,
            n_recommendations=request.n_recommendations,
            period_col='period',
            score_col='normalized_score',
            inflection=request.inflection,
            steepness=request.steepness,
            random_seed=request.random_seed
        )
    else:
        recommendations = recommend_threads_exponential(
            df,
            n_recommendations=request.n_recommendations,
            period_col='period',
            score_col='normalized_score',
            decay_constant=request.decay_constant,
            random_seed=request.random_seed
        )
    
    # Merge with original thread data
    result_df = recommendations.merge(df, on='thread_id', how='left')
    
    return {
        "method": "logistic" if request.use_logistic else "exponential",
        "n_recommendations": request.n_recommendations,
        "recommendations": [
            {
                "thread_id": int(row.thread_id),
                "probability": float(row.probability),
                "sample_order": int(row.sample_order),
                "likes": int(row.likes),
                "dislikes": int(row.dislikes),
                "replies": int(row.replies),
                "reposts": int(row.reposts),
                "other_interactions": int(row.other_interactions),
                "cursory_views": int(row.cursory_views),
                "engaged_views": int(row.engaged_views),
                "age_minutes": int(row.age_minutes),
                "normalized_score": float(row.normalized_score),
            }
            for _, row in result_df.iterrows()
        ]
    } 