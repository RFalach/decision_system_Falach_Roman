import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from models import Score, Criterion, Rule
from services.convolution import get_ranking, compare_all_methods


def render_tab_results():
    st.header("Результати та Аналіз")

    method_map = {
        "Адитивна згортка": "additive",
        "Мультиплікативна згортка": "multiplicative",
        "Обережна (мінімаксна) згортка": "minimax",
    }

    col_method, col_calc = st.columns([3, 1])
    with col_method:
        method_name = st.selectbox("Метод згортки:", list(method_map.keys()))
    with col_calc:
        st.write("")
        st.write("")
        calc_btn = st.button("Розрахувати", type="primary")

    if calc_btn:
        st.session_state["calc_done"] = True
        st.session_state["method"] = method_map[method_name]

    if st.session_state.get("calc_done"):
        method_key = st.session_state.get("method", "additive")
        ranking = get_ranking(method_key)

        if ranking is not None and "Меч" in ranking.columns:
            from services.rules import apply_all_rules
            matrix_after = apply_all_rules(Score.get_matrix())

            col_rank, col_explain = st.columns([3, 2])

            with col_rank:
                st.subheader("Рейтинг мечів")
                st.dataframe(ranking, use_container_width=True)

                best_sword = ranking.iloc[0]["Меч"]
                best_score = ranking.iloc[0]["Оцінка"]
                st.success(f"Найкращий меч: {best_sword} (оцінка: {best_score:.4f})")

            with col_explain:
                st.subheader("Пояснення рішення")

                criteria = Criterion.get_all()
                sorted_criteria = sorted(criteria, key=lambda c: c["weight"], reverse=True)
                top_criteria = sorted_criteria[:3]

                st.write(f"{best_sword} обрано як найкращий.")
                st.write("Найвпливовіші критерії:")
                for c in top_criteria:
                    st.write(f"- {c['name']} (вага: {c['weight']:.2f}, тип: {c['type']})")

                rules = Rule.get_all()
                active_rules = [r for r in rules if r["is_active"]]
                if active_rules:
                    st.write("Застосовані правила:")
                    for r in active_rules:
                        st.write(f"- IF {r['condition']} THEN {r['action']}")
                else:
                    st.write("Правила не застосовано.")

            with st.expander("Матриця після застосування правил"):
                st.dataframe(matrix_after, use_container_width=True)
        else:
            st.warning("Немає даних для розрахунку. Додайте мечі та критерії.")

    st.divider()
    st.subheader("Аналіз чутливості")

    criteria = Criterion.get_all()
    if criteria:
        crit_names = [c["name"] for c in criteria]
        selected_crit = st.selectbox("Змінити вагу критерію:", crit_names)

        original_criterion = next((c for c in criteria if c["name"] == selected_crit), None)
        if original_criterion:
            original_weight = original_criterion["weight"]
            new_weight = st.slider(
                "Нова вага:",
                0.0, 0.5, original_weight, 0.01,
                key="sensitivity"
            )

            Criterion.update_weight(original_criterion["id"], new_weight)
            ranking_new = get_ranking("additive")
            Criterion.update_weight(original_criterion["id"], original_weight)

            if ranking_new is not None and "Меч" in ranking_new.columns:
                fig, ax = plt.subplots(figsize=(10, 5))
                swords = ranking_new["Меч"].tolist()
                scores = ranking_new["Оцінка"].tolist()
                colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(swords)))
                ax.barh(swords[::-1], scores[::-1], color=colors[::-1])
                ax.set_xlabel("Інтегральна оцінка")
                ax.set_title(f"Змiна рейтингу при вазi {selected_crit} = {new_weight:.2f}")
                st.pyplot(fig)
            else:
                st.warning("Недостатньо даних для аналізу чутливості")

    st.divider()
    with st.expander("Порівняння методів згортки"):
        if st.button("Порівняти всі методи"):
            comparison = compare_all_methods()
            st.dataframe(comparison, use_container_width=True)
