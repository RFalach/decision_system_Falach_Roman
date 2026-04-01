from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["decision_system"]

def get_alternatives():
    return list(db.alternatives.find())

def get_criteria():
    return list(db.criteria.find())

def get_evaluations():
    return list(db.evaluations.find())

def add_alternative(name):
    alt = {"name": name}
    result = db.alternatives.insert_one(alt)
    return result.inserted_id


def add_evaluation(alt_id, crit_id, value):
    db.evaluations.insert_one({
        "alternative_id": alt_id,
        "criterion_id": crit_id,
        "value": value
    })
