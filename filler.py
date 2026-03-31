from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["decision_system"]


db.alternatives.delete_many({})
db.criteria.delete_many({})
db.evaluations.delete_many({})


alternatives = [
    {"_id": 1, "name": "Laptop A"},
    {"_id": 2, "name": "Laptop B"},
    {"_id": 3, "name": "Laptop C"},
    {"_id": 4, "name": "Laptop D"},
    {"_id": 5, "name": "Laptop E"},
    {"_id": 6, "name": "Laptop F"},
    {"_id": 7, "name": "Laptop G"},
    {"_id": 8, "name": "Laptop H"},
    {"_id": 9, "name": "Laptop I"},
    {"_id": 10, "name": "Laptop J"},
]

db.alternatives.insert_many(alternatives)


criteria = [
    {"_id": 1, "name": "Price", "type": "min"},
    {"_id": 2, "name": "Performance", "type": "max"},
    {"_id": 3, "name": "Battery", "type": "max"},
    {"_id": 4, "name": "Weight", "type": "min"}
]

db.criteria.insert_many(criteria)


evaluations = [
    # Laptop A
    {"alternative_id":1,"criterion_id":1,"value":500},
    {"alternative_id":1,"criterion_id":2,"value":6},
    {"alternative_id":1,"criterion_id":3,"value":7},
    {"alternative_id":1,"criterion_id":4,"value":2.5},

    # Laptop B
    {"alternative_id":2,"criterion_id":1,"value":1200},
    {"alternative_id":2,"criterion_id":2,"value":10},
    {"alternative_id":2,"criterion_id":3,"value":5},
    {"alternative_id":2,"criterion_id":4,"value":2.8},

    # Laptop C
    {"alternative_id":3,"criterion_id":1,"value":800},
    {"alternative_id":3,"criterion_id":2,"value":8},
    {"alternative_id":3,"criterion_id":3,"value":9},
    {"alternative_id":3,"criterion_id":4,"value":2.3},

    # Laptop D
    {"alternative_id":4,"criterion_id":1,"value":1000},
    {"alternative_id":4,"criterion_id":2,"value":7},
    {"alternative_id":4,"criterion_id":3,"value":10},
    {"alternative_id":4,"criterion_id":4,"value":1.5},

    # Laptop E
    {"alternative_id":5,"criterion_id":1,"value":900},
    {"alternative_id":5,"criterion_id":2,"value":8},
    {"alternative_id":5,"criterion_id":3,"value":8},
    {"alternative_id":5,"criterion_id":4,"value":2.1},

    # Laptop F
    {"alternative_id":6,"criterion_id":1,"value":600},
    {"alternative_id":6,"criterion_id":2,"value":6},
    {"alternative_id":6,"criterion_id":3,"value":7},
    {"alternative_id":6,"criterion_id":4,"value":2.4},

    # Laptop G
    {"alternative_id":7,"criterion_id":1,"value":1100},
    {"alternative_id":7,"criterion_id":2,"value":9},
    {"alternative_id":7,"criterion_id":3,"value":6},
    {"alternative_id":7,"criterion_id":4,"value":2.0},

    # Laptop H
    {"alternative_id":8,"criterion_id":1,"value":950},
    {"alternative_id":8,"criterion_id":2,"value":7},
    {"alternative_id":8,"criterion_id":3,"value":9},
    {"alternative_id":8,"criterion_id":4,"value":1.3},

    # Laptop I
    {"alternative_id":9,"criterion_id":1,"value":1300},
    {"alternative_id":9,"criterion_id":2,"value":10},
    {"alternative_id":9,"criterion_id":3,"value":7},
    {"alternative_id":9,"criterion_id":4,"value":2.7},

    # Laptop J
    {"alternative_id":10,"criterion_id":1,"value":400},
    {"alternative_id":10,"criterion_id":2,"value":5},
    {"alternative_id":10,"criterion_id":3,"value":6},
    {"alternative_id":10,"criterion_id":4,"value":2.6},
]

db.evaluations.insert_many(evaluations)

print("data added")
