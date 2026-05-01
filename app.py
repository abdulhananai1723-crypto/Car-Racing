import streamlit as st
import random
import time

st.set_page_config(page_title="Car Racing Game", layout="centered")

if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "player_lane" not in st.session_state:
    st.session_state.player_lane = 1
if "game_running" not in st.session_state:
    st.session_state.game_running = False

st.title("🚗 Car Racing Game")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Left"):
        st.session_state.player_lane = max(0, st.session_state.player_lane - 1)

with col2:
    if st.button("Start / Restart"):
        st.session_state.game_running = True
        st.session_state.score = 0

with col3:
    if st.button("Right ➡️"):
        st.session_state.player_lane = min(2, st.session_state.player_lane + 1)

game_area = st.empty()

if st.session_state.game_running:
    obstacle_lane = random.randint(0, 2)

    st.session_state.score += 1

    road = ""
    for row in range(6):
        road += "<div style='display:flex; justify-content:center;'>"
        for lane in range(3):
            car = "⬛"
            if row == 1 and lane == obstacle_lane:
                car = "🚙"
            if row == 5 and lane == st.session_state.player_lane:
                car = "🚗"
            road += f"<div style='font-size:35px; width:70px; text-align:center;'>{car}</div>"
        road += "</div>"

    game_area.markdown(
        f"""
        <div style="
            background:#222;
            padding:20px;
            border-radius:12px;
            color:white;
            text-align:center;
        ">
            {road}
            <h3>Score: {st.session_state.score}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if obstacle_lane == st.session_state.player_lane and st.session_state.score > 2:
        st.session_state.game_running = False
        st.error(f"Game Over! Score: {st.session_state.score}")

        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
    else:
        time.sleep(0.4)
        st.rerun()

st.write(f"🏆 High Score: {st.session_state.high_score}")
