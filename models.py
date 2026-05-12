from db import get_connection

class Sword:
    @staticmethod
    def get_all():
        conn = get_connection()
        swords = conn.execute("SELECT * FROM swords").fetchall()
        conn.close()
        return [dict(s) for s in swords]
    
    @staticmethod
    def add(name):
        conn = get_connection()
        try:
            conn.execute("INSERT INTO swords (name) VALUES (?)", (name,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()
    
    @staticmethod
    def delete(sword_id):
        conn = get_connection()
        conn.execute("DELETE FROM swords WHERE id = ?", (sword_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update(sword_id, name):
        conn = get_connection()
        conn.execute("UPDATE swords SET name=? WHERE id=?", (name, sword_id))
        conn.commit()
        conn.close()

class Criterion:
    @staticmethod
    def get_all():
        conn = get_connection()
        criteria = conn.execute("SELECT * FROM criteria").fetchall()
        conn.close()
        return [dict(c) for c in criteria]
    
    @staticmethod
    def add(name, crit_type="maximize", weight=0.0, unit=""):
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO criteria (name, type, weight, unit) VALUES (?, ?, ?, ?)",
                (name, crit_type, weight, unit)
            )
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()
    
    @staticmethod
    def delete(criterion_id):
        conn = get_connection()
        conn.execute("DELETE FROM criteria WHERE id = ?", (criterion_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_weight(criterion_id, weight):
        conn = get_connection()
        conn.execute("UPDATE criteria SET weight=? WHERE id=?", (weight, criterion_id))
        conn.commit()
        conn.close()

class Score:
    @staticmethod
    def set_score(sword_id, criterion_id, value):
        conn = get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO scores (sword_id, criterion_id, value) 
            VALUES (?, ?, ?)
        """, (sword_id, criterion_id, value))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_matrix():
        import pandas as pd
        conn = get_connection()
        
        swords = conn.execute("SELECT id, name FROM swords").fetchall()
        criteria = conn.execute("SELECT id, name FROM criteria").fetchall()
        
        data = {}
        for s in swords:
            row = {}
            for c in criteria:
                score = conn.execute(
                    "SELECT value FROM scores WHERE sword_id=? AND criterion_id=?",
                    (s["id"], c["id"])
                ).fetchone()
                row[c["name"]] = score["value"] if score else 0.0
            data[s["name"]] = row
        
        conn.close()
        return pd.DataFrame.from_dict(data, orient='index')

class Rule:
    @staticmethod
    def get_all():
        conn = get_connection()
        rules = conn.execute("SELECT * FROM rules").fetchall()
        conn.close()
        return [dict(r) for r in rules]
    
    @staticmethod
    def add(condition, action):
        conn = get_connection()
        conn.execute(
            "INSERT INTO rules (condition, action) VALUES (?, ?)",
            (condition, action)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(rule_id):
        conn = get_connection()
        conn.execute("DELETE FROM rules WHERE id=?", (rule_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def toggle(rule_id):
        conn = get_connection()
        current = conn.execute("SELECT is_active FROM rules WHERE id=?", (rule_id,)).fetchone()
        new_status = 0 if current["is_active"] else 1
        conn.execute("UPDATE rules SET is_active=? WHERE id=?", (new_status, rule_id))
        conn.commit()
        conn.close()
