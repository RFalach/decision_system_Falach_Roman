from db import init_db, get_connection
from models import Sword, Criterion, Score

def load_sample_data():
    existing_swords = Sword.get_all()
    if existing_swords:
        return
    
    swords_names = [
        "Claymore",
        "Man-Serpent Greatsword",
        "Black Knight Sword",
        "Moonlight Greatsword",
        "Zweihander",
        "Estoc",
        "Priscilla's Dagger",
        "Astora's Straight Sword",
    ]
    
    for name in swords_names:
        Sword.add(name)
    
    criteria_data = [
        ("Ціна", "minimize", 0.12, "монет"),
        ("Міцність", "maximize", 0.10, "од."),
        ("Вага", "minimize", 0.08, "кг"),
        ("Необхідна Сила", "minimize", 0.10, "од."),
        ("Необхідна Спритність", "minimize", 0.10, "од."),
        ("Скейл від Сили", "maximize", 0.10, "ранг"),
        ("Скейл від Спритності", "maximize", 0.10, "ранг"),
        ("Фізична Шкода", "maximize", 0.12, "од."),
        ("Вогняна Шкода", "maximize", 0.10, "од."),
        ("Магічна Шкода", "maximize", 0.08, "од."),
    ]
    
    for name, crit_type, weight, unit in criteria_data:
        Criterion.add(name, crit_type, weight, unit)
    
    # Скейли: S=5, A=4, B=3, C=2, D=1, E=0
    swords = Sword.get_all()
    criteria = Criterion.get_all()
    
    sword_dict = {s["name"]: s["id"] for s in swords}
    crit_dict = {c["name"]: c["id"] for c in criteria}
    
    scores_data = {
        "Claymore": {
            "Ціна": 3000,
            "Міцність": 75,
            "Вага": 5.0,
            "Необхідна Сила": 16,
            "Необхідна Спритність": 10,
            "Скейл від Сили": 3,
            "Скейл від Спритності": 2,
            "Фізична Шкода": 130,
            "Вогняна Шкода": 0,
            "Магічна Шкода": 0
        },
        "Man-Serpent Greatsword": {
            "Ціна": 4500,
            "Міцність": 85,
            "Вага": 7.5,
            "Необхідна Сила": 24,
            "Необхідна Спритність": 0,
            "Скейл від Сили": 5,
            "Скейл від Спритності": 0,
            "Фізична Шкода": 190,
            "Вогняна Шкода": 0,
            "Магічна Шкода": 0
        },
        "Black Knight Sword": {
            "Ціна": 6000,
            "Міцність": 80,
            "Вага": 6.0,
            "Необхідна Сила": 20,
            "Необхідна Спритність": 18,
            "Скейл від Сили": 4,
            "Скейл від Спритності": 3,
            "Фізична Шкода": 160,
            "Вогняна Шкода": 35,
            "Магічна Шкода": 0
        },
        "Moonlight Greatsword": {
            "Ціна": 8000,
            "Міцність": 60,
            "Вага": 5.5,
            "Необхідна Сила": 16,
            "Необхідна Спритність": 10,
            "Скейл від Сили": 2,
            "Скейл від Спритності": 0,
            "Фізична Шкода": 80,
            "Вогняна Шкода": 0,
            "Магічна Шкода": 140
        },
        "Zweihander": {
            "Ціна": 3500,
            "Міцність": 90,
            "Вага": 10.0,
            "Необхідна Сила": 24,
            "Необхідна Спритність": 8,
            "Скейл від Сили": 4,
            "Скейл від Спритності": 1,
            "Фізична Шкода": 200,
            "Вогняна Шкода": 0,
            "Магічна Шкода": 0
        },
        "Estoc": {
            "Ціна": 2000,
            "Міцність": 55,
            "Вага": 2.0,
            "Необхідна Сила": 8,
            "Необхідна Спритність": 16,
            "Скейл від Сили": 1,
            "Скейл від Спритності": 4,
            "Фізична Шкода": 90,
            "Вогняна Шкода": 0,
            "Магічна Шкода": 0
        },
        "Priscilla's Dagger": {
            "Ціна": 5000,
            "Міцність": 30,
            "Вага": 1.0,
            "Необхідна Сила": 6,
            "Необхідна Спритність": 20,
            "Скейл від Сили": 0,
            "Скейл від Спритності": 5,
            "Фізична Шкода": 70,
            "Вогняна Шкода": 0,
            "Магічна Шкода": 25
        },
        "Astora's Straight Sword": {
            "Ціна": 2500,
            "Міцність": 65,
            "Вага": 3.0,
            "Необхідна Сила": 12,
            "Необхідна Спритність": 12,
            "Скейл від Сили": 3,
            "Скейл від Спритності": 3,
            "Фізична Шкода": 110,
            "Вогняна Шкода": 0,
            "Магічна Шкода": 20
        },
    }
    
    for sword_name, scores in scores_data.items():
        sword_id = sword_dict[sword_name]
        for crit_name, value in scores.items():
            crit_id = crit_dict[crit_name]
            Score.set_score(sword_id, crit_id, value)
    
    print("data added")

if __name__ == "__main__":
    init_db()
    load_sample_data()
