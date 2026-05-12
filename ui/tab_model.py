import streamlit as st
import pandas as pd
from models import Sword, Criterion, Score

def render_tab_model():
    st.header("Модель та Дані")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Альтернативи (Мечі)")
        
        with st.form("add_sword_form"):
            new_name = st.text_input("Назва меча:")
            if st.form_submit_button("Додати"):
                if new_name:
                    if Sword.add(new_name):
                        st.success(f"Меч '{new_name}' додано!")
                        st.rerun()
                    else:
                        st.error("Такий меч уже існує!")
        
        swords = Sword.get_all()
        if swords:
            df_swords = pd.DataFrame(swords)[["id", "name"]]
            df_swords.columns = ["ID", "Назва"]
            st.dataframe(df_swords, use_container_width=True, hide_index=True)
            
            delete_id = st.selectbox(
                "Видалити меч:", 
                [s["id"] for s in swords], 
                format_func=lambda x: next((s["name"] for s in swords if s["id"] == x), "")
            )
            if st.button("Видалити"):
                Sword.delete(delete_id)
                st.rerun()
        else:
            st.info("Немає мечів. Додайте перший!")
    
    with col_right:
        st.subheader("Критерії")
        
        with st.form("add_criterion_form"):
            new_crit_name = st.text_input("Назва критерію:")
            col_type, col_unit = st.columns(2)
            with col_type:
                crit_type = st.selectbox(
                    "Тип:", 
                    ["maximize", "minimize"], 
                    format_func=lambda x: "maximize" if x == "maximize" else "minimize"
                )
            with col_unit:
                crit_unit = st.text_input("Одиниці виміру:")
            crit_weight = st.slider("Вага:", 0.0, 1.0, 0.1, 0.01, format="%.2f")
            if st.form_submit_button("Додати критерій"):
                if new_crit_name:
                    Criterion.add(new_crit_name, crit_type, crit_weight, crit_unit)
                    st.rerun()
        
        criteria = Criterion.get_all()
        if criteria:
            df_crit = pd.DataFrame(criteria)[["id", "name", "type", "weight", "unit"]]
            df_crit.columns = ["ID", "Назва", "Тип", "Вага", "Од."]
            st.dataframe(df_crit, use_container_width=True, hide_index=True)
        else:
            st.info("Немає критеріїв.")
    
    st.divider()
    st.subheader("Матриця оцінювання")
    
    matrix = Score.get_matrix()
    if not matrix.empty:
        st.dataframe(matrix, use_container_width=True)
    else:
        st.warning("Матриця порожня. Додайте мечі, критерії та оцінки.")
    
    st.divider()
    with st.expander("Визначення ваг через голосування"):
        st.write("Тут буде імпорт результатів голосування з Google Таблиць")
        st.write("Методи: більшість, Борда, вагове голосування, рангове")
