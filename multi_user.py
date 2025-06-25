import uuid
import pandas as pd
import random

def assign_users_to_threads(df: pd.DataFrame, num_unique_users: int = 100) -> pd.DataFrame:

    threads_df_multi_user = df.copy()

    user_ids = []
    for _ in range(100):
        user_ids.append(str(uuid.uuid4())) #generate 100 users using uuids, and assign them to each post using random sampling

    threads_df_multi_user['user_id'] = random.choices(user_ids, k=len(threads_df_multi_user))
    return threads_df_multi_user


if __name__ == "__main__":
    df = pd.read_csv('threads_scored.csv')
    threads_df_with_users = assign_users_to_threads(df)
