import numpy as np
import pandas as pd
from models import Score, Criterion, Sword
from services.rules import apply_all_rules


def _get_data():
    matrix = Score.get_matrix()
    criteria = Criterion.get_all()
    
    matrix = apply_all_rules(matrix)
    
    weights = {}
    crit_types = {}
    for c in criteria:
        weights[c["name"]] = c["weight"]
        crit_types[c["name"]] = c["type"]
    
    return matrix, weights, crit_types


def _normalize(matrix, crit_types):
    df = matrix.copy()
    
    for col in df.columns:
        values = df[col].values.astype(float)
        min_val = values.min()
        max_val = values.max()
        
        if max_val == min_val:
            df[col] = 0.5
        else:
            if crit_types.get(col) == "maximize":
                df[col] = (values - min_val) / (max_val - min_val)
            else:
                df[col] = (max_val - values) / (max_val - min_val)
    
    return df


def _apply_weights(normalized_matrix, weights):
    df = normalized_matrix.copy()
    for col in df.columns:
        w = weights.get(col, 0.1)
        df[col] = df[col] * w
    return df


def additive():
    matrix, weights, crit_types = _get_data()
    if matrix.empty:
        return None
    
    norm = _normalize(matrix, crit_types)
    weighted = _apply_weights(norm, weights)
    scores = weighted.sum(axis=1)
    ranking = scores.sort_values(ascending=False)
    return ranking


def multiplicative():
    matrix, weights, crit_types = _get_data()
    if matrix.empty:
        return None
    
    norm = _normalize(matrix, crit_types)
    epsilon = 0.01
    norm_safe = norm + epsilon
    
    scores = pd.Series(index=norm.index, dtype=float)
    for idx in norm.index:
        product = 1.0
        for col in norm.columns:
            w = weights.get(col, 0.1)
            product *= norm_safe.loc[idx, col] ** w
        scores[idx] = product
    
    ranking = scores.sort_values(ascending=False)
    return ranking


def minimax():
    matrix, weights, crit_types = _get_data()
    if matrix.empty:
        return None
    
    norm = _normalize(matrix, crit_types)
    norm = norm + 0.01
    
    scores = pd.Series(index=norm.index, dtype=float)
    for idx in norm.index:
        worst_score = float('inf')
        for col in norm.columns:
            w = weights.get(col, 0.1)
            if w > 0:
                score = norm.loc[idx, col] * w
                if score < worst_score:
                    worst_score = score
        scores[idx] = worst_score if worst_score != float('inf') else 0.0
    
    ranking = scores.sort_values(ascending=False)
    return ranking


def get_ranking(method="additive"):
    methods = {
        "additive": additive,
        "multiplicative": multiplicative,
        "minimax": minimax,
    }
    
    func = methods.get(method, additive)
    ranking = func()
    
    if ranking is None or len(ranking) == 0:
        return pd.DataFrame({"Помилка": ["Немає даних для розрахунку або всі альтернативи відсіяні"]})
    
    result = pd.DataFrame({
        "Місце": range(1, len(ranking) + 1),
        "Меч": ranking.index,
        "Оцінка": ranking.values.round(4)
    })
    result = result.set_index("Місце")
    return result


def compare_all_methods():
    methods = {
        "Адитивна": additive,
        "Мультиплікативна": multiplicative,
        "Обережна": minimax,
    }
    
    results = {}
    for name, func in methods.items():
        ranking = func()
        if ranking is not None and len(ranking) > 0:
            results[name] = list(ranking.index)
    
    if not results:
        return pd.DataFrame({"Помилка": ["Немає даних"]})
    
    return pd.DataFrame(results)
