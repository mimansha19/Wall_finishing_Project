const API_URL = "http://localhost:8000/trajectories/";
const canvas = document.getElementById("coverageCanvas");
const ctx = canvas.getContext("2d");
const playBtn = document.getElementById("playBtn");

let trajectoryPoints = [];
let animationId = null;
let currentIndex = 0;
let wallWidthGlob = 5;
let wallHeightGlob = 5;

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function drawObstacle(obs, wallWidth, wallHeight) {
  const x = (obs.x / wallWidth) * canvas.width;
  const y = canvas.height - ((obs.y + obs.h) / wallHeight) * canvas.height;
  const w = (obs.w / wallWidth) * canvas.width;
  const h = (obs.h / wallHeight) * canvas.height;
  ctx.fillStyle = "rgba(200, 0, 0, 0.5)";
  ctx.fillRect(x, y, w, h);
}

function drawTrajectorySegment(
  points,
  wallWidth,
  wallHeight,
  startIdx,
  endIdx,
  strokeColor
) {
  if (endIdx <= startIdx) return;
  ctx.strokeStyle = strokeColor;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = startIdx; i < endIdx; i++) {
    const [mx, my] = points[i];
    const x = (mx / wallWidth) * canvas.width;
    const y = canvas.height - (my / wallHeight) * canvas.height;
    if (i === startIdx) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  }
  ctx.stroke();
}

function drawRobotDot(point, wallWidth, wallHeight) {
  const [mx, my] = point;
  const x = (mx / wallWidth) * canvas.width;
  const y = canvas.height - (my / wallHeight) * canvas.height;
  ctx.fillStyle = "red";
  ctx.beginPath();
  ctx.arc(x, y, 5, 0, 2 * Math.PI);
  ctx.fill();
}

async function generateCoverage() {
  const wallWidth = parseFloat(document.getElementById("wallWidth").value);
  const wallHeight = parseFloat(document.getElementById("wallHeight").value);
  const obsX = parseFloat(document.getElementById("obsX").value);
  const obsY = parseFloat(document.getElementById("obsY").value);
  const obsW = parseFloat(document.getElementById("obsW").value);
  const obsH = parseFloat(document.getElementById("obsH").value);

  wallWidthGlob = wallWidth;
  wallHeightGlob = wallHeight;

  const payload = {
    wall_width: wallWidth,
    wall_height: wallHeight,
    obstacles: [{ x: obsX, y: obsY, w: obsW, h: obsH }],
    step: 0.5,
  };

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    trajectoryPoints = data.data;
    clearCanvas();
    drawObstacle(payload.obstacles[0], wallWidth, wallHeight);

    drawTrajectorySegment(
      trajectoryPoints,
      wallWidth,
      wallHeight,
      0,
      trajectoryPoints.length,
      "blue"
    );
    playBtn.disabled = false;
  } catch (error) {
    console.error("Error generating coverage:", error);
  }
}

document
  .getElementById("generateBtn")
  .addEventListener("click", generateCoverage);

function playTrajectory() {
  if (trajectoryPoints.length === 0) return;
  playBtn.disabled = true;
  currentIndex = 0;

  function step() {
    if (currentIndex > trajectoryPoints.length) {
      cancelAnimationFrame(animationId);
      playBtn.disabled = false;
      return;
    }

    clearCanvas();

    const obsX = parseFloat(document.getElementById("obsX").value);
    const obsY = parseFloat(document.getElementById("obsY").value);
    const obsW = parseFloat(document.getElementById("obsW").value);
    const obsH = parseFloat(document.getElementById("obsH").value);
    drawObstacle(
      { x: obsX, y: obsY, w: obsW, h: obsH },
      wallWidthGlob,
      wallHeightGlob
    );

    drawTrajectorySegment(
      trajectoryPoints,
      wallWidthGlob,
      wallHeightGlob,
      0,
      currentIndex,
      "yellow"
    );

    drawTrajectorySegment(
      trajectoryPoints,
      wallWidthGlob,
      wallHeightGlob,
      currentIndex,
      trajectoryPoints.length,
      "blue"
    );

    if (currentIndex < trajectoryPoints.length) {
      drawRobotDot(
        trajectoryPoints[currentIndex],
        wallWidthGlob,
        wallHeightGlob
      );
    }

    currentIndex++;
    animationId = requestAnimationFrame(step);
  }

  animationId = requestAnimationFrame(step);
}

playBtn.addEventListener("click", playTrajectory);
