import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Car Racing Game", layout="centered")

st.title("🏁 Professional Car Racing Game")

game_code = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    background: linear-gradient(135deg, #111827, #1f2937);
    font-family: Arial, sans-serif;
    text-align: center;
    color: white;
}

.game-wrapper {
    width: 430px;
    margin: auto;
    padding: 18px;
    border-radius: 22px;
    background: #0f172a;
    box-shadow: 0 20px 45px rgba(0,0,0,0.45);
}

.top-bar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    font-size: 16px;
    font-weight: bold;
}

.controls {
    margin: 10px 0 15px;
    font-size: 14px;
    color: #cbd5e1;
}

button {
    background: linear-gradient(135deg, #ef4444, #f97316);
    color: white;
    border: none;
    padding: 11px 28px;
    border-radius: 999px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 8px 18px rgba(239,68,68,0.35);
}

button:hover {
    transform: scale(1.03);
}

canvas {
    border-radius: 18px;
    border: 4px solid #334155;
    background: #111;
}
</style>
</head>

<body>

<div class="game-wrapper">
    <div class="top-bar">
        <div>Score: <span id="score">0</span></div>
        <div>Level: <span id="level">1</span></div>
        <div>High: <span id="high">0</span></div>
    </div>

    <button onclick="startGame()">Start / Restart</button>

    <div class="controls">
        Press <b>A</b> for Left &nbsp; | &nbsp; Press <b>D</b> for Right
    </div>

    <canvas id="gameCanvas" width="400" height="600"></canvas>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const scoreEl = document.getElementById("score");
const levelEl = document.getElementById("level");
const highEl = document.getElementById("high");

let roadX = 65;
let roadWidth = 270;
let laneWidth = roadWidth / 3;

let player = {
    lane: 1,
    y: 495,
    width: 48,
    height: 78
};

let enemies = [];

let score = 0;
let highScore = 0;
let level = 1;
let speed = 4;
let gameRunning = false;
let animationId = null;
let roadOffset = 0;
let frameCount = 0;

function laneCenter(lane) {
    return roadX + laneWidth * lane + laneWidth / 2;
}

function updateUI() {
    scoreEl.textContent = score;
    levelEl.textContent = level;
    highEl.textContent = highScore;
}

function createEnemy() {
    enemies.push({
        lane: Math.floor(Math.random() * 3),
        y: -100,
        width: 48,
        height: 78,
        passed: false
    });
}

function drawCar(x, y, color, isPlayer=false) {
    ctx.save();

    ctx.fillStyle = "rgba(0,0,0,0.35)";
    ctx.beginPath();
    ctx.ellipse(x, y + 78, 34, 10, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x - 24, y, 48, 78, 10);
    ctx.fill();

    ctx.fillStyle = isPlayer ? "#93c5fd" : "#fecaca";
    ctx.beginPath();
    ctx.roundRect(x - 16, y + 10, 32, 18, 5);
    ctx.fill();

    ctx.fillStyle = isPlayer ? "#bfdbfe" : "#fee2e2";
    ctx.beginPath();
    ctx.roundRect(x - 15, y + 38, 30, 16, 5);
    ctx.fill();

    ctx.fillStyle = "#020617";
    ctx.fillRect(x - 31, y + 12, 8, 18);
    ctx.fillRect(x + 23, y + 12, 8, 18);
    ctx.fillRect(x - 31, y + 50, 8, 18);
    ctx.fillRect(x + 23, y + 50, 8, 18);

    ctx.fillStyle = isPlayer ? "#fde047" : "#f8fafc";
    ctx.fillRect(x - 15, y + 70, 9, 5);
    ctx.fillRect(x + 6, y + 70, 9, 5);

    ctx.restore();
}

function drawRoad() {
    ctx.fillStyle = "#16a34a";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#1f2937";
    ctx.fillRect(roadX, 0, roadWidth, canvas.height);

    ctx.fillStyle = "#111827";
    ctx.fillRect(roadX + 10, 0, roadWidth - 20, canvas.height);

    ctx.strokeStyle = "#f8fafc";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(roadX, 0);
    ctx.lineTo(roadX, canvas.height);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(roadX + roadWidth, 0);
    ctx.lineTo(roadX + roadWidth, canvas.height);
    ctx.stroke();

    ctx.setLineDash([35, 28]);
    ctx.lineDashOffset = -roadOffset;
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 3;

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

function checkCollision(enemy) {
    const playerX = laneCenter(player.lane);
    const enemyX = laneCenter(enemy.lane);

    return (
        Math.abs(playerX - enemyX) < 42 &&
        enemy.y + enemy.height > player.y + 8 &&
        enemy.y < player.y + player.height - 8
    );
}

function drawStartScreen() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawRoad();
    drawCar(laneCenter(player.lane), player.y, "#2563eb", true);

    ctx.fillStyle = "rgba(15,23,42,0.78)";
    ctx.fillRect(45, 205, 310, 165);

    ctx.fillStyle = "white";
    ctx.font = "bold 30px Arial";
    ctx.fillText("READY TO RACE", 70, 265);

    ctx.font = "17px Arial";
    ctx.fillText("Press Start, then use A / D", 90, 310);
}

function gameOver() {
    gameRunning = false;
    highScore = Math.max(highScore, score);
    updateUI();

    ctx.fillStyle = "rgba(0,0,0,0.72)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "white";
    ctx.font = "bold 42px Arial";
    ctx.fillText("GAME OVER", 72, 270);

    ctx.font = "22px Arial";
    ctx.fillText("Score: " + score, 150, 320);
    ctx.fillText("Click Start to play again", 92, 365);
}

function gameLoop() {
    if (!gameRunning) return;

    frameCount++;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    roadOffset += speed;
    if (roadOffset > 65) roadOffset = 0;

    drawRoad();

    if (frameCount % 90 === 0) {
        createEnemy();
    }

    for (let i = enemies.length - 1; i >= 0; i--) {
        let enemy = enemies[i];
        enemy.y += speed;

        drawCar(laneCenter(enemy.lane), enemy.y, "#dc2626", false);

        if (!enemy.passed && enemy.y > player.y + player.height) {
            enemy.passed = true;
            score += 1;

            if (score % 5 === 0) {
                level += 1;
                speed += 0.6;
            }

            updateUI();
        }

        if (enemy.y > canvas.height + 120) {
            enemies.splice(i, 1);
        }

        if (checkCollision(enemy)) {
            gameOver();
            return;
        }
    }

    drawCar(laneCenter(player.lane), player.y, "#2563eb", true);

    animationId = requestAnimationFrame(gameLoop);
}

function startGame() {
    cancelAnimationFrame(animationId);

    player.lane = 1;
    enemies = [];
    score = 0;
    level = 1;
    speed = 4;
    frameCount = 0;
    roadOffset = 0;
    gameRunning = true;

    createEnemy();
    updateUI();
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

drawStartScreen();
updateUI();
</script>

</body>
</html>
"""

components.html(game_code, height=760)
