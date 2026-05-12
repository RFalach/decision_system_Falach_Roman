import numpy as np
import pandas as pd
from models import Criterion

def majority_voting(votes_df):
    criteria = Criterion.get_all()
    crit_names = [c["name"] for c in criteria]
    weights = {name: 0.0 for name in crit_names}

    for _, row in votes_df.iterrows():
        top_crit = row.get("best_criterion")
        if top_crit and top_crit in weights:
            weights[top_crit] += 1

    total = sum(weights.values())
    if total > 0:
        for name in weights:
            weights[name] = round(weights[name] / total, 4)

    return weights

def borda_count(votes_df):
    criteria = Criterion.get_all()
    crit_names = [c["name"] for c in criteria]
    n = len(crit_names)
    scores = {name: 0.0 for name in crit_names}

    for _, row in votes_df.iterrows():
        rankings = row.get("rankings", "")
        if isinstance(rankings, str):
            ranked_list = [r.strip() for r in rankings.split(",")]
            for rank_idx, crit_name in enumerate(ranked_list):
                if crit_name in scores:
                    scores[crit_name] += n - rank_idx - 1

    total = sum(scores.values())
    if total > 0:
        for name in scores:
            scores[name] = round(scores[name] / total, 4)

    return scores

def rank_voting(votes_df):
    criteria = Criterion.get_all()
    crit_names = [c["name"] for c in criteria]
    n = len(crit_names)
    scores = {name: 0.0 for name in crit_names}

    for _, row in votes_df.iterrows():
        rankings = row.get("rankings", "")
        if isinstance(rankings, str):
            ranked_list = [r.strip() for r in rankings.split(",")]
            for rank_idx, crit_name in enumerate(ranked_list):
                if crit_name in scores:
                    scores[crit_name] += 1 / (rank_idx + 1)

    total = sum(scores.values())
    if total > 0:
        for name in scores:
            scores[name] = round(scores[name] / total, 4)

    return scores

def weighted_voting(votes_df):
    criteria = Criterion.get_all()
    crit_names = [c["name"] for c in criteria]
    scores = {name: 0.0 for name in crit_names}

    for _, row in votes_df.iterrows():
        expert_weight = row.get("expert_weight", 1.0)
        top_crit = row.get("best_criterion")
        if top_crit and top_crit in scores:
            scores[top_crit] += expert_weight

    total = sum(scores.values())
    if total > 0:
        for name in scores:
            scores[name] = round(scores[name] / total, 4)

    return scores

def calculate_voting(votes_df, method="majority"):
    methods = {
        "majority": majority_voting,
        "borda": borda_count,
        "rank": rank_voting,
        "weighted": weighted_voting,
    }

    func = methods.get(method, majority_voting)
    return func(votes_df)

def apply_voting_weights(weights):
    criteria = Criterion.get_all()
    for c in criteria:
        if c["name"] in weights:
            Criterion.update_weight(c["id"], weights[c["name"]])
