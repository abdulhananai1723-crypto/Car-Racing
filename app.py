import streamlit as st
import random
import time

st.set_page_config(page_title="Car Racing Game", layout="centered")

# Session state
if "game_running" not in st.session_state:
    st.session_state.game_running = False
    st.session_state.score = 0
    st.session_state.high_score = 0

st.title("🚗 Car Racing Game")

# Start Button
if st.button("Start Game", key="start_btn"):
    st.session_state.game_running = True
    st.session_state.score = 0

# Restart Button
if st.button("Restart Game", key="restart_btn"):
    st.session_state.score = 0
    st.session_state.game_running = True

# Game logic simulation
if st.session_state.game_running:
    game_area = st.empty()

    for i in range(100):
        st.session_state.score += 1
        speed = 0.05 - min(st.session_state.score * 0.0002, 0.04)

        game_area.markdown(
            f"""
            <div style="
                background-color:#222;
                height:300px;
                border-radius:10px;
                color:white;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:20px;">
                🚗 Avoid Cars! Score: {st.session_state.score}
            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(speed)

    st.session_state.game_running = False
    st.success(f"Game Over! Score: {st.session_state.score}")

    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score

st.write(f"🏆 High Score: {st.session_state.high_score}")
