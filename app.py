import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Car Racing Game", layout="centered")

st.title("🚗 Car Racing Game")

game_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        background: transparent;
        text-align: center;
        font-family: Arial, sans-serif;
    }

    canvas {
        background: #1e1e1e;
        border-radius: 15px;
        border: 5px solid #444;
    }

    button {
        margin: 10px;
        padding: 10px 25px;
        font-size: 16px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        background: #ff4757;
        color: white;
        font-weight: bold;
    }

    .info {
        color: #222;
        font-size: 18px;
        margin-bottom: 10px;
    }
</style>
</head>

<body>

<div class="info">
    Press <b>A</b> to move left | Press <b>D</b> to move right
</div>

<button onclick="startGame()">Start / Restart</button>

<br>

<canvas id="gameCanvas" width="400" height="600"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let roadX = 70;
let roadWidth = 260;
let laneWidth = roadWidth / 3;

let player = {
    lane: 1,
    y: 500,
    width: 55,
    height: 90
};

let enemy = {
    lane: Math.floor(Math.random() * 3),
    y: -120,
    width: 55,
    height: 90,
    speed: 5
};

let score = 0;
let highScore = 0;
let gameRunning = false;
let animationId;
let roadLineY = 0;

function laneCenter(lane) {
    return roadX + laneWidth * lane + laneWidth / 2;
}

function drawCar(x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x - 25, y, 50, 80);

    ctx.fillStyle = "#111";
    ctx.fillRect(x - 18, y + 10, 36, 18);

    ctx.fillStyle = "#87ceeb";
    ctx.fillRect(x - 15, y + 35, 30, 18);

    ctx.fillStyle = "black";
    ctx.fillRect(x - 32, y + 12, 10, 20);
    ctx.fillRect(x + 22, y + 12, 10, 20);
    ctx.fillRect(x - 32, y + 52, 10, 20);
    ctx.fillRect(x + 22, y + 52, 10, 20);

    ctx.fillStyle = "yellow";
    ctx.fillRect(x - 18, y + 72, 10, 6);
    ctx.fillRect(x + 8, y + 72, 10, 6);
}

function drawRoad() {
    ctx.fillStyle = "#2c2c2c";
    ctx.fillRect(roadX, 0, roadWidth, canvas.height);

    ctx.fillStyle = "#00aa00";
    ctx.fillRect(0, 0, roadX, canvas.height);
    ctx.fillRect(roadX + roadWidth, 0, roadX, canvas.height);

    ctx.strokeStyle = "white";
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.moveTo(roadX, 0);
    ctx.lineTo(roadX, canvas.height);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(roadX + roadWidth, 0);
    ctx.lineTo(roadX + roadWidth, canvas.height);
    ctx.stroke();

    ctx.setLineDash([30, 25]);
    ctx.lineDashOffset = -roadLineY;
    ctx.strokeStyle = "#f1f1f1";

    ctx.beginPath();
    ctx.moveTo(roadX + laneWidth, 0);
    ctx.lineTo(roadX + laneWidth, canvas.height);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(roadX + laneWidth * 2, 0);
    ctx.lineTo(roadX + laneWidth * 2, canvas.height);
    ctx.stroke();

    ctx.setLineDash([]);
}

function drawText() {
    ctx.fillStyle = "white";
    ctx.font = "22px Arial";
    ctx.fillText("Score: " + score, 15, 35);
    ctx.fillText("High: " + highScore, 285, 35);
}

function collision() {
    let playerX = laneCenter(player.lane);
    let enemyX = laneCenter(enemy.lane);

    return (
        Math.abs(playerX - enemyX) < 45 &&
        enemy.y + enemy.height > player.y &&
        enemy.y < player.y + player.height
    );
}

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    roadLineY += enemy.speed;
    if (roadLineY > 55) roadLineY = 0;

    drawRoad();

    enemy.y += enemy.speed;

    if (enemy.y > canvas.height) {
        enemy.y = -120;
        enemy.lane = Math.floor(Math.random() * 3);
        score++;

        if (score % 5 === 0) {
            enemy.speed += 0.7;
        }
    }

    drawCar(laneCenter(enemy.lane), enemy.y, "#ff3838");
    drawCar(laneCenter(player.lane), player.y, "#1e90ff");
    drawText();

    if (collision()) {
        gameRunning = false;
        highScore = Math.max(highScore, score);

        ctx.fillStyle = "rgba(0,0,0,0.7)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "white";
        ctx.font = "38px Arial";
        ctx.fillText("GAME OVER", 95, 270);

        ctx.font = "22px Arial";
        ctx.fillText("Score: " + score, 155, 315);
        ctx.fillText("Press Start to Restart", 95, 360);

        return;
    }

    if (gameRunning) {
        animationId = requestAnimationFrame(gameLoop);
    }
}

function startGame() {
    cancelAnimationFrame(animationId);

    player.lane = 1;
    enemy.lane = Math.floor(Math.random() * 3);
    enemy.y = -120;
    enemy.speed = 5;
    score = 0;
    gameRunning = true;

    gameLoop();
}

document.addEventListener("keydown", function(event) {
    if (!gameRunning) return;

    if (event.key === "a" || event.key === "A") {
        player.lane = Math.max(0, player.lane - 1);
    }

    if (event.key === "d" || event.key === "D") {
        player.lane = Math.min(2, player.lane + 1);
    }
});

drawRoad();
drawCar(laneCenter(player.lane), player.y, "#1e90ff");
drawText();
</script>

</body>
</html>
"""

components.html(game_code, height=720)
