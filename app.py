import streamlit as st
import random

st.set_page_config(page_title="Car Racing Game", layout="centered")

if "player_lane" not in st.session_state:
    st.session_state.player_lane = 1
if "enemy_lane" not in st.session_state:
    st.session_state.enemy_lane = random.randint(0, 2)
if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🚗 Car Racing Game")

if st.button("Start / Restart"):
    st.session_state.player_lane = 1
    st.session_state.enemy_lane = random.randint(0, 2)
    st.session_state.score = 0
    st.session_state.game_over = False

col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Left"):
        st.session_state.player_lane = max(0, st.session_state.player_lane - 1)

with col2:
    if st.button("Right ➡️"):
        st.session_state.player_lane = min(2, st.session_state.player_lane + 1)

if not st.session_state.game_over:
    st.session_state.score += 1

    if st.session_state.score % 3 == 0:
        st.session_state.enemy_lane = random.randint(0, 2)

    road = ""

    for row in range(6):
        road += "<div style='display:flex; justify-content:center;'>"

        for lane in range(3):
            item = "⬛"

            if row == 1 and lane == st.session_state.enemy_lane:
                item = "🚙"

            if row == 5 and lane == st.session_state.player_lane:
                item = "🚗"

            road += f"""
            <div style='
                width:80px;
                height:55px;
                font-size:35px;
                text-align:center;
            '>{item}</div>
            """

        road += "</div>"

    st.markdown(
        f"""
        <div style="
            background:#222;
            padding:25px;
            border-radius:12px;
            color:white;
            width:330px;
            margin:auto;
        ">
            {road}
        </div>
        <h3 style="text-align:center;">Score: {st.session_state.score}</h3>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.enemy_lane == st.session_state.player_lane:
        st.session_state.game_over = True
        st.session_state.high_score = max(
            st.session_state.high_score,
            st.session_state.score
        )
        st.error("Game Over! Car crashed.")

else:
    st.error("Game Over! Press Start / Restart.")

st.write(f"🏆 High Score: {st.session_state.high_score}")
