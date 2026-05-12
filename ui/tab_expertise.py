import streamlit as st
import pandas as pd
from models import Sword, Criterion
from services.experts import calculate_agreement, apply_agreed_ratings
from db import get_connection


def render_tab_expertise():
    st.header("Експертиза")

    st.write("Завантажте CSV-файл з оцінками експертів або введіть дані вручну.")

    st.subheader("Завантаження даних")
    uploaded_file = st.file_uploader(
        "Завантажте CSV-файл (колонки: expert_name, sword_name, criterion_name, rating)",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Завантажено {len(df)} записів")
            st.dataframe(df, use_container_width=True)

            if st.button("Зберегти в базу даних", type="primary"):
                conn = get_connection()
                swords = Sword.get_all()
                criteria = Criterion.get_all()
                sword_map = {s["name"]: s["id"] for s in swords}
                crit_map = {c["name"]: c["id"] for c in criteria}

                saved = 0
                for _, row in df.iterrows():
                    try:
                        expert = row.get("expert_name") or row.get("Експерт")
                        sword_name = row.get("sword_name") or row.get("Меч")
                        crit_name = row.get("criterion_name") or row.get("Критерій")
                        rating = float(row.get("rating") or row.get("Оцінка"))

                        if sword_name in sword_map and crit_name in crit_map:
                            conn.execute(
                                "INSERT INTO expert_ratings (expert_name, sword_id, criterion_id, rating) VALUES (?, ?, ?, ?)",
                                (expert, sword_map[sword_name], crit_map[crit_name], rating)
                            )
                            saved += 1
                    except (ValueError, TypeError):
                        continue

                conn.commit()
                conn.close()
                st.success(f"Збережено {saved} оцінок")
                st.rerun()
        except Exception as e:
            st.error(f"Помилка читання файлу: {e}")

    st.divider()

    with st.expander("Або ввести оцінки вручну"):
        manual_data = st.text_area(
            "Формат: Експерт, Назва меча, Назва критерію, Оцінка",
            placeholder="Експерт1, Claymore, Фізична Шкода, 9"
        )
        if st.button("Зберегти введені оцінки"):
            if manual_data.strip():
                conn = get_connection()
                swords = Sword.get_all()
                criteria = Criterion.get_all()
                sword_map = {s["name"]: s["id"] for s in swords}
                crit_map = {c["name"]: c["id"] for c in criteria}

                saved = 0
                for line in manual_data.strip().split("\n"):
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) == 4:
                        expert, sword_name, crit_name, rating = parts
                        try:
                            rating = float(rating)
                            if sword_name in sword_map and crit_name in crit_map:
                                conn.execute(
                                    "INSERT INTO expert_ratings (expert_name, sword_id, criterion_id, rating) VALUES (?, ?, ?, ?)",
                                    (expert, sword_map[sword_name], crit_map[crit_name], rating)
                                )
                                saved += 1
                        except ValueError:
                            continue

                conn.commit()
                conn.close()
                st.success(f"Збережено {saved} оцінок")
                st.rerun()

    st.divider()

    st.subheader("Методи узгодження експертних оцінок")

    method_map = {
        "Коефіцієнт конкордації Кендалла (W)": "kendall",
        "Коефіцієнт варіації": "variation",
        "Середнє квадратичне відхилення": "msd",
    }

    col1, col2 = st.columns([2, 1])
    with col1:
        agreement_method = st.selectbox("Оберіть метод перевірки узгодженості:", list(method_map.keys()))
    with col2:
        st.write("")
        st.write("")
        check_btn = st.button("Перевірити узгодженість", type="primary")

    if check_btn:
        conn = get_connection()
        ratings = pd.read_sql("SELECT * FROM expert_ratings", conn)
        conn.close()

        if ratings.empty:
            st.warning("Немає даних для перевірки. Завантажте оцінки експертів.")
        else:
            method_key = method_map[agreement_method]
            coefficient = calculate_agreement(ratings, method_key)
            st.session_state["agreement_coefficient"] = coefficient
            st.session_state["ratings_data"] = ratings
            st.session_state["agreement_checked"] = True

    if st.session_state.get("agreement_checked"):
        coefficient = st.session_state.get("agreement_coefficient", 0)
        st.metric("Коефіцієнт узгодженості", f"{coefficient:.4f}")

        if coefficient >= 0.7:
            st.success("Узгодженість достатня. Можна використовувати усереднені оцінки.")
            if st.button("Застосувати узгоджені оцінки до матриці"):
                ratings = st.session_state.get("ratings_data")
                apply_agreed_ratings(ratings)
                st.session_state["agreement_checked"] = False
                st.success("Оцінки застосовано!")
                st.rerun()
        elif coefficient >= 0.5:
            st.warning("Узгодженість середня. Рекомендується перевірити дані.")
        else:
            st.error("Узгодженість низька. Дані не рекомендується використовувати.")
