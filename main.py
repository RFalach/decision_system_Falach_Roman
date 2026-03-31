from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["decision_system"]


alternatives = list(db.alternatives.find())
criteria = list(db.criteria.find())
evaluations = list(db.evaluations.find())


weights = {
    1: 0.3,  # Price
    2: 0.3,  # Performance
    3: 0.2,  # Battery
    4: 0.2   # Weight
}


scores = {a["_id"]: 0 for a in alternatives}


for crit in criteria:
    crit_id = crit["_id"]
    crit_type = crit["type"]

    values = [e["value"] for e in evaluations if e["criterion_id"] == crit_id]
    max_val = max(values)
    min_val = min(values)
    
    for e in evaluations:
        if e["criterion_id"] == crit_id:
            if crit_type == "max":
                norm = e["value"] / max_val
            else:
                norm = min_val / e["value"]
            scores[e["alternative_id"]] += norm * weights[crit_id]

sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print("rating:")
for i, (alt_id, score) in enumerate(sorted_scores, start=1):
    alt = db.alternatives.find_one({"_id": alt_id})
    print(f"{i}. {alt['name']} — {round(score, 3)}")

best = db.alternatives.find_one({"_id": sorted_scores[0][0]})
print("\nbest option:", best["name"])
