import streamlit as st
import pandas as pd
from models import Rule, Criterion

def render_tab_rules():
    st.header("Експертні Правила (IF-THEN)")
    
    st.markdown("""
    Тут ви можете задати правила, які впливають на відбір мечів.
    Наприклад, відсіяти надто важкі мечі або скоригувати оцінки.
    """)
    
    st.subheader("Порогові обмеження (відтинання)")
    
    criteria = Criterion.get_all()
    if criteria:
        col_crit, col_op, col_val = st.columns([2, 1, 1])
        with col_crit:
            thresh_crit = st.selectbox("Критерій:", [c["name"] for c in criteria])
        with col_op:
            thresh_op = st.selectbox("Оператор:", [">", "<", ">=", "<=", "=="])
        with col_val:
            thresh_val = st.number_input("Значення:", value=0.0, step=0.1)
        
        if st.button("Додати порогове обмеження"):
            condition = f"{thresh_crit} {thresh_op} {thresh_val}"
            Rule.add(condition, "ВИКЛЮЧИТИ")
            st.rerun()
    
    st.divider()
    st.subheader("Правила корекції IF-THEN")
    
    col_if, col_then = st.columns(2)
    with col_if:
        rule_condition = st.text_input("ЯКЩО (IF):", placeholder="Вага (кг) > 6")
    with col_then:
        rule_action = st.text_input("ТОДІ (THEN):", placeholder="Зменшити оцінку на 30%")
    
    if st.button("➕ Додати правило"):
        if rule_condition and rule_action:
            Rule.add(rule_condition, rule_action)
            st.rerun()
    
    st.divider()
    st.subheader("Активні правила")
    
    rules = Rule.get_all()
    if rules:
        for rule in rules:
            status = "✅" if rule["is_active"] else "❌"
            col_rule, col_btn = st.columns([4, 1])
            with col_rule:
                st.write(f"{status} **IF** {rule['condition']} **THEN** {rule['action']}")
            with col_btn:
                if st.button("🔄" if rule["is_active"] else "▶️", key=f"rule_{rule['id']}"):
                    Rule.toggle(rule["id"])
                    st.rerun()
        
        if st.button("Очистити всі правила"):
            for rule in rules:
                Rule.delete(rule["id"])
            st.rerun()
    else:
        st.info("Правил поки немає. Додайте перше!")
