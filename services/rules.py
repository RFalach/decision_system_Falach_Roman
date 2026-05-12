import pandas as pd
import re
from models import Rule


def apply_thresholds(matrix):
    rules = Rule.get_all()
    threshold_rules = [r for r in rules if r["is_active"] and "ВИКЛЮЧИТИ" in r["action"].upper()]

    excluded = set()
    for rule in threshold_rules:
        condition = rule["condition"]
        for sword_name in matrix.index:
            try:
                parts = condition.split()
                if len(parts) < 3:
                    continue
                crit_name_parts = parts[:-2]
                crit_name = " ".join(crit_name_parts)
                operator = parts[-2]
                threshold = float(parts[-1])

                if crit_name in matrix.columns:
                    value = matrix.loc[sword_name, crit_name]
                    if operator == ">" and value > threshold:
                        excluded.add(sword_name)
                    elif operator == "<" and value < threshold:
                        excluded.add(sword_name)
                    elif operator == ">=" and value >= threshold:
                        excluded.add(sword_name)
                    elif operator == "<=" and value <= threshold:
                        excluded.add(sword_name)
                    elif operator == "==" and value == threshold:
                        excluded.add(sword_name)
            except (ValueError, IndexError):
                continue

    return matrix.drop(index=excluded, errors="ignore")


def apply_corrections(matrix):
    rules = Rule.get_all()
    correction_rules = [r for r in rules if r["is_active"] and "ВИКЛЮЧИТИ" not in r["action"].upper()]

    corrected = matrix.copy()
    for rule in correction_rules:
        condition = rule["condition"]
        action = rule["action"]
        for sword_name in corrected.index:
            try:
                parts = condition.split()
                if len(parts) < 3:
                    continue
                crit_name_parts = parts[:-2]
                crit_name = " ".join(crit_name_parts)
                operator = parts[-2]
                threshold = float(parts[-1])

                if crit_name in corrected.columns:
                    value = corrected.loc[sword_name, crit_name]
                    condition_met = False
                    if operator == ">" and value > threshold:
                        condition_met = True
                    elif operator == "<" and value < threshold:
                        condition_met = True
                    elif operator == ">=" and value >= threshold:
                        condition_met = True
                    elif operator == "<=" and value <= threshold:
                        condition_met = True

                    if condition_met:
                        action_lower = action.lower()
                        if "зменшити" in action_lower:
                            percent_match = re.search(r"(\d+)%", action)
                            if percent_match:
                                percent = float(percent_match.group(1)) / 100
                                corrected.loc[sword_name, crit_name] *= (1 - percent)
                        elif "збільшити" in action_lower:
                            percent_match = re.search(r"(\d+)%", action)
                            if percent_match:
                                percent = float(percent_match.group(1)) / 100
                                corrected.loc[sword_name, crit_name] *= (1 + percent)
            except (ValueError, IndexError):
                continue

    return corrected


def apply_all_rules(matrix):
    filtered = apply_thresholds(matrix)
    corrected = apply_corrections(filtered)
    return corrected
