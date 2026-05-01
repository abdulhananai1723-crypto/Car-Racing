import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Lucky Car Racing Game", layout="centered")

st.title("🏁 Lucky Car Racing Game")

game_code = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    background: transparent;
    font-family: Arial, sans-serif;
}

.wrapper {
    width: 430px;
    margin: auto;
    background: linear-gradient(180deg, #020617, #111827);
    border-radius: 24px;
    padding: 18px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.45);
    color: white;
    text-align: center;
}

.hud {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    font-weight: bold;
    font-size: 16px;
}

.controls {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-bottom: 12px;
}

button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    transform: scale(1.05);
}

.hint {
    color: #cbd5e1;
    font-size: 14px;
    margin-bottom: 12px;
}

canvas {
    border-radius: 18px;
    border: 4px solid #475569;
    background: #111827;
}
</style>
</head>

<body>

<div class="wrapper">
    <div class="hud">
        <div>Score: <span id="score">0</span></div>
        <div>Level: <span id="level">1</span></div>
        <div>High: <span id="high">0</span></div>
    </div>

    <div class="controls">
        <button onclick="moveLeft()">⬅ Left</button>
        <button onclick="startGame()">▶ Start / Restart</button>
        <button onclick="moveRight()">Right ➡</button>
    </div>

    <div class="hint">
        Press <b>Enter</b> to Start / Restart &nbsp; | &nbsp;
        <b>A</b> Left &nbsp; | &nbsp; <b>D</b> Right
    </div>

    <canvas id="gameCanvas" width="400" height="600"></canvas>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const scoreEl = document.getElementById("score");
const levelEl = document.getElementById("level");
const highEl = document.getElementById("high");

let roadX = 60;
let roadWidth = 280;
let laneWidth = roadWidth / 3;

let player = {
    lane: 1,
    y: 500,
    width: 46,
    height: 78
};

let enemies = [];
let coins = [];

let score = 0;
let highScore = 0;
let level = 1;
let speed = 4;
let frame = 0;
let roadOffset = 0;
let gameRunning = false;
let animationId = null;

function updateHUD() {
    scoreEl.innerText = score;
    levelEl.innerText = level;
    highEl.innerText = highScore;
}

function laneCenter(lane) {
    return roadX + laneWidth * lane + laneWidth / 2;
}

function moveLeft() {
    if (!gameRunning) return;
    player.lane = Math.max(0, player.lane - 1);
}

function moveRight() {
    if (!gameRunning) return;
    player.lane = Math.min(2, player.lane + 1);
}

function drawRoundedRect(x, y, w, h, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, r);
    ctx.fill();
}

function drawCar(x, y, color, playerCar=false) {
    ctx.save();

    ctx.fillStyle = "rgba(0,0,0,0.35)";
    ctx.beginPath();
    ctx.ellipse(x, y + 80, 32, 10, 0, 0, Math.PI * 2);
    ctx.fill();

    drawRoundedRect(x - 24, y, 48, 78, 10, color);

    drawRoundedRect(x - 15, y + 10, 30, 16, 5, playerCar ? "#93c5fd" : "#fecaca");
    drawRoundedRect(x - 16, y + 38, 32, 16, 5, playerCar ? "#bfdbfe" : "#fee2e2");

    ctx.fillStyle = "#020617";
    ctx.fillRect(x - 31, y + 12, 8, 18);
    ctx.fillRect(x + 23, y + 12, 8, 18);
    ctx.fillRect(x - 31, y + 50, 8, 18);
    ctx.fillRect(x + 23, y + 50, 8, 18);

    ctx.fillStyle = playerCar ? "#fde047" : "#f8fafc";
    ctx.fillRect(x - 14, y + 70, 9, 5);
    ctx.fillRect(x + 5, y + 70, 9, 5);

    ctx.restore();
}

function drawRoad() {
    ctx.fillStyle = "#15803d";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#14532d";
    for (let i = 0; i < 20; i++) {
        ctx.beginPath();
        ctx.arc(25, i * 45 + roadOffset, 10, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(375, i * 45 + roadOffset, 10, 0, Math.PI * 2);
        ctx.fill();
    }

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

function createEnemy() {
    enemies.push({
        lane: Math.floor(Math.random() * 3),
        y: -110,
        passed: false
    });
}

function createCoin() {
    coins.push({
        lane: Math.floor(Math.random() * 3),
        y: -50,
        collected: false
    });
}

function checkCarCollision(enemy) {
    let px = laneCenter(player.lane);
    let ex = laneCenter(enemy.lane);

    return (
        Math.abs(px - ex) < 42 &&
        enemy.y + 78 > player.y + 10 &&
        enemy.y < player.y + 68
    );
}

function drawCoin(x, y) {
    ctx.fillStyle = "#facc15";
    ctx.beginPath();
    ctx.arc(x, y, 13, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#ca8a04";
    ctx.font = "bold 16px Arial";
    ctx.fillText("$", x - 5, y + 6);
}

function drawStartScreen() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawRoad();
    drawCar(laneCenter(player.lane), player.y, "#2563eb", true);

    ctx.fillStyle = "rgba(2,6,23,0.82)";
    ctx.fillRect(45, 190, 310, 190);

    ctx.fillStyle = "white";
    ctx.font = "bold 34px Arial";
    ctx.fillText("READY?", 135, 255);

    ctx.font = "18px Arial";
    ctx.fillText("Press ENTER to Start", 110, 305);
    ctx.fillText("A = Left    D = Right", 118, 340);
}

function gameOver() {
    gameRunning = false;
    highScore = Math.max(highScore, score);
    updateHUD();

    ctx.fillStyle = "rgba(0,0,0,0.75)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "white";
    ctx.font = "bold 42px Arial";
    ctx.fillText("GAME OVER", 70, 265);

    ctx.font = "22px Arial";
    ctx.fillText("Score: " + score, 150, 320);
    ctx.fillText("Press ENTER to restart", 88, 365);
}

function gameLoop() {
    if (!gameRunning) return;

    frame++;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    roadOffset += speed;
    if (roadOffset > 65) roadOffset = 0;

    drawRoad();

    if (frame % 85 === 0) {
        createEnemy();
    }

    if (frame % 140 === 0) {
        createCoin();
    }

    for (let i = enemies.length - 1; i >= 0; i--) {
        let e = enemies[i];
        e.y += speed;

        drawCar(laneCenter(e.lane), e.y, "#dc2626", false);

        if (!e.passed && e.y > player.y + 80) {
            e.passed = true;
            score += 1;

            if (score % 5 === 0) {
                level++;
                speed += 0.5;
            }

            updateHUD();
        }

        if (e.y > canvas.height + 120) {
            enemies.splice(i, 1);
        }

        if (checkCarCollision(e)) {
            gameOver();
            return;
        }
    }

    for (let i = coins.length - 1; i >= 0; i--) {
        let c = coins[i];
        c.y += speed;

        drawCoin(laneCenter(c.lane), c.y);

        if (
            c.lane === player.lane &&
            c.y > player.y &&
            c.y < player.y + 80 &&
            !c.collected
        ) {
            c.collected = true;
            score += 2;
            updateHUD();
            coins.splice(i, 1);
        }

        if (c.y > canvas.height + 50) {
            coins.splice(i, 1);
        }
    }

    drawCar(laneCenter(player.lane), player.y, "#2563eb", true);

    animationId = requestAnimationFrame(gameLoop);
}

function startGame() {
    cancelAnimationFrame(animationId);

    player.lane = 1;
    enemies = [];
    coins = [];
    score = 0;
    level = 1;
    speed = 4;
    frame = 0;
    roadOffset = 0;
    gameRunning = true;

    createEnemy();
    updateHUD();
    gameLoop();
}

document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        startGame();
    }

    if (event.key === "a" || event.key === "A") {
        moveLeft();
    }

    if (event.key === "d" || event.key === "D") {
        moveRight();
    }
});

drawStartScreen();
updateHUD();
</script>

</body>
</html>
"""

components.html(game_code, height=760)
