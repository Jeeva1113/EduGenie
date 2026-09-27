const result = document.getElementById("result");

document.querySelectorAll(".tab").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    button.classList.add("active");
    document.getElementById(button.dataset.target).classList.add("active");
  });
});

async function request(path, body) {
  result.textContent = "Thinking…";
  const response = await fetch(path, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Request failed");
  return data;
}

async function runQA() {
  try {
    const data = await request("/api/qa", {question: document.getElementById("qaInput").value});
    result.textContent = data.result;
  } catch (e) { result.textContent = e.message; }
}

async function runExplain() {
  try {
    const data = await request("/api/explain", {topic: document.getElementById("explainInput").value});
    result.textContent = data.result;
  } catch (e) { result.textContent = e.message; }
}

async function runSummary() {
  try {
    const data = await request("/api/summarize", {text: document.getElementById("summaryInput").value});
    result.textContent = data.result;
  } catch (e) { result.textContent = e.message; }
}

async function runQuiz() {
  try {
    const data = await request("/api/quiz", {topic: document.getElementById("quizInput").value});
    const box = document.getElementById("quizResult");
    box.innerHTML = data.questions.map((q, i) => `
      <div class="quiz-question">
        <strong>${i + 1}. ${escapeHtml(q.question)}</strong>
        <ol type="A">${q.options.map(o => `<li>${escapeHtml(o)}</li>`).join("")}</ol>
        <p><b>Answer:</b> ${escapeHtml(q.answer)}</p>
        <p>${escapeHtml(q.explanation)}</p>
      </div>
    `).join("");
    result.textContent = "Quiz generated successfully.";
  } catch (e) { result.textContent = e.message; }
}

async function runPath() {
  try {
    const data = await request("/api/learning-path", {goal: document.getElementById("pathInput").value});
    document.getElementById("pathResult").innerHTML =
      `<ol>${data.steps.map(s => `<li>${escapeHtml(s)}</li>`).join("")}</ol>`;
    result.textContent = "Learning path generated successfully.";
  } catch (e) { result.textContent = e.message; }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
  }[c]));
}

fetch("/api/health")
  .then(r => r.json())
  .then(() => document.getElementById("status").textContent = "API Online")
  .catch(() => document.getElementById("status").textContent = "API Offline");
