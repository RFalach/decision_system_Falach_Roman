from data import *
from service import calculate_scores

alternatives = get_alternatives()
criteria = get_criteria()
evaluations = get_evaluations()

scores = calculate_scores(alternatives, criteria, evaluations)

sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print("RATING:")
for i, (alt_id, score) in enumerate(sorted_scores, start=1):
    alt = next(a for a in alternatives if a["_id"] == alt_id)
    print(f"{i}. {alt['name']} — {round(score, 3)}")

best = next(a for a in alternatives if a["_id"] == sorted_scores[0][0])

print("\nBEST OPTION:", best["name"])
