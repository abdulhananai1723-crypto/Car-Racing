import streamlit as st
import random

st.set_page_config(page_title="Car Racing Game", layout="centered")

# Initialize session
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.player_lane = 1
    st.session_state.enemy_lane = random.randint(0, 2)
    st.session_state.enemy_row = 0
    st.session_state.score = 0
    st.session_state.high_score = 0
    st.session_state.game_over = False

st.title("🚗 Car Racing Game")

# Functions
def restart():
    st.session_state.started = True
    st.session_state.player_lane = 1
    st.session_state.enemy_lane = random.randint(0, 2)
    st.session_state.enemy_row = 0
    st.session_state.score = 0
    st.session_state.game_over = False

def move_left():
    st.session_state.player_lane = max(0, st.session_state.player_lane - 1)

def move_right():
    st.session_state.player_lane = min(2, st.session_state.player_lane + 1)

# Buttons
col1, col2, col3 = st.columns(3)

with col1:
    st.button("⬅️ Left", on_click=move_left)

with col2:
    st.button("Start / Restart", on_click=restart)

with col3:
    st.button("Right ➡️", on_click=move_right)

# Game
if st.session_state.started and not st.session_state.game_over:

    st.session_state.enemy_row += 1

    if st.session_state.enemy_row > 5:
        st.session_state.enemy_row = 0
        st.session_state.enemy_lane = random.randint(0, 2)
        st.session_state.score += 1

    # Collision
    if (
        st.session_state.enemy_row == 5
        and st.session_state.enemy_lane == st.session_state.player_lane
    ):
        st.session_state.game_over = True
        st.session_state.high_score = max(
            st.session_state.high_score,
            st.session_state.score
        )

    # Build road (FIXED)
    road = "<table style='margin:auto;'>"

    for row in range(6):
        road += "<tr>"

        for lane in range(3):
            item = "⬛"

            if row == st.session_state.enemy_row and lane == st.session_state.enemy_lane:
                item = "🚙"

            if row == 5 and lane == st.session_state.player_lane:
                item = "🚗"

            road += f"<td style='width:70px;height:55px;text-align:center;font-size:34px;'>{item}</td>"

        road += "</tr>"

    road += "</table>"

    html = f"""
    <div style="
        background:#222;
        padding:25px;
        border-radius:12px;
        width:330px;
        margin:auto;
        color:white;
    ">
        {road}
        <h2 style="text-align:center;">Score: {st.session_state.score}</h2>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

    st.button("Next Frame ▶️")

elif st.session_state.game_over:
    st.error("💥 Game Over! Press Start / Restart")

st.write(f"🏆 High Score: {st.session_state.high_score}")
