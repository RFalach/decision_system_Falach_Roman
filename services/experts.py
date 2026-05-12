import numpy as np
import pandas as pd
from models import Score, Sword, Criterion

def kendall_concordance(ratings_df):
    if ratings_df.empty:
        return 0.0, None

    pivoted = ratings_df.pivot_table(
        index=["expert_name", "sword_id"],
        columns="criterion_id",
        values="rating",
        aggfunc="mean"
    )

    experts = ratings_df["expert_name"].unique()
    m = len(experts)
    n = len(ratings_df[["sword_id", "criterion_id"]].drop_duplicates())

    if m < 2 or n < 2:
        return 0.0, None

    ranks = ratings_df.groupby("expert_name")["rating"].rank(method="average")
    ratings_df_copy = ratings_df.copy()
    ratings_df_copy["rank"] = ranks

    rank_sums = ratings_df_copy.groupby(["sword_id", "criterion_id"])["rank"].sum()
    mean_rank_sum = rank_sums.mean()
    S = ((rank_sums - mean_rank_sum) ** 2).sum()

    max_S = (m ** 2 * (n ** 3 - n)) / 12
    if max_S == 0:
        return 0.0, None

    W = S / max_S
    return round(W, 4), ratings_df_copy

def coefficient_of_variation(ratings_df):
    if ratings_df.empty:
        return 0.0

    grouped = ratings_df.groupby(["sword_id", "criterion_id"])["rating"]
    means = grouped.mean()
    stds = grouped.std()
    cvs = (stds / means.replace(0, np.nan)).fillna(0)
    avg_cv = cvs.mean()
    return round(1 - avg_cv, 4)

def mean_square_deviation(ratings_df):
    if ratings_df.empty:
        return 0.0

    grouped = ratings_df.groupby(["sword_id", "criterion_id"])["rating"]
    means = grouped.mean()

    deviations = []
    for (sword_id, crit_id), group in grouped:
        mean_val = means.loc[(sword_id, crit_id)]
        deviations.extend((group - mean_val) ** 2)

    if not deviations:
        return 0.0

    msd = np.sqrt(np.mean(deviations))
    max_rating = ratings_df["rating"].max()
    min_rating = ratings_df["rating"].min()
    norm_msd = msd / (max_rating - min_rating) if max_rating > min_rating else 0
    return round(1 - norm_msd, 4)

def calculate_agreement(ratings_df, method="kendall"):
    methods = {
        "kendall": kendall_concordance,
        "variation": coefficient_of_variation,
        "msd": mean_square_deviation,
    }

    func = methods.get(method, kendall_concordance)
    result = func(ratings_df)

    if method == "kendall":
        return result[0]
    return result

def apply_agreed_ratings(ratings_df):
    if ratings_df.empty:
        return

    averaged = ratings_df.groupby(["sword_id", "criterion_id"])["rating"].mean().reset_index()

    for _, row in averaged.iterrows():
        Score.set_score(
            sword_id=int(row["sword_id"]),
            criterion_id=int(row["criterion_id"]),
            value=round(row["rating"], 2)
        )
