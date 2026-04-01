def calculate_scores(alternatives, criteria, evaluations):
    scores = {a["_id"]: 0 for a in alternatives}

    for crit in criteria:
        crit_id = crit["_id"]
        crit_type = crit["type"]
        weight = crit.get("weight", 0.25)

        crit_values = [e for e in evaluations if e["criterion_id"] == crit_id]
        
        if not crit_values:
            continue

        values = [e["value"] for e in crit_values]

        max_val = max(values)
        min_val = min(values)

        for e in crit_values:
            if crit_type == "max":
                norm = e["value"] / max_val if max_val != 0 else 0
            else:
                norm = min_val / e["value"] if e["value"] != 0 else 0

            scores[e["alternative_id"]] += norm * weight

    return scores
