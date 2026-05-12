import streamlit as st
from db import init_db
from sample_data import load_sample_data
from ui.tab_expertise import render_tab_expertise
from ui.tab_model import render_tab_model
from ui.tab_rules import render_tab_rules
from ui.tab_results import render_tab_results

init_db()
load_sample_data()

st.set_page_config(
    page_title="СППР - Вибір Фентезійного Меча",
    layout="wide"
)

st.title("СППР - Вибір Фентезійного Меча")
st.caption("Система підтримки прийняття рішень для RPG-гравців")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Експертиза",
    "2. Модель та Дані",
    "3. Правила (IF-THEN)",
    "4. Результати та Аналіз"
])

with tab1:
    render_tab_expertise()

with tab2:
    render_tab_model()

with tab3:
    render_tab_rules()

with tab4:
    render_tab_results()
