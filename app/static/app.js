const form = document.querySelector("#analysisForm");
const rewriteButton = document.querySelector("#rewriteButton");
const statusText = document.querySelector("#statusText");
const matchScore = document.querySelector("#matchScore");
const atsScore = document.querySelector("#atsScore");
const yearsExperience = document.querySelector("#yearsExperience");
const missingSkills = document.querySelector("#missingSkills");
const atsRecommendations = document.querySelector("#atsRecommendations");
const resumeSuggestions = document.querySelector("#resumeSuggestions");
const resumePreview = document.querySelector("#resumePreview");

function setStatus(text) {
  statusText.textContent = text;
}

function renderList(element, items) {
  element.innerHTML = "";
  if (!items || items.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No items found.";
    element.appendChild(li);
    return;
  }
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    element.appendChild(li);
  });
}

function renderChips(items) {
  missingSkills.innerHTML = "";
  if (!items || items.length === 0) {
    const span = document.createElement("span");
    span.className = "chip";
    span.textContent = "No major gaps";
    missingSkills.appendChild(span);
    return;
  }
  items.forEach((item) => {
    const span = document.createElement("span");
    span.className = "chip";
    span.textContent = item;
    missingSkills.appendChild(span);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("Analyzing...");
  rewriteButton.disabled = true;

  const formData = new FormData(form);
  const response = await fetch("/resume/analyze", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    setStatus("Analysis failed");
    return;
  }

  const payload = await response.json();
  matchScore.textContent = `${payload.analysis.score}%`;
  atsScore.textContent = `${payload.ats.score}%`;
  yearsExperience.textContent =
    payload.years_experience_estimate === null
      ? "Review"
      : `${payload.years_experience_estimate} yrs`;
  renderChips(payload.analysis.missing_skills);
  renderList(atsRecommendations, payload.ats.recommendations);
  renderList(resumeSuggestions, payload.analysis.suggestions);
  resumePreview.textContent = payload.resume_preview;
  setStatus("Analysis complete");
  rewriteButton.disabled = false;
});

rewriteButton.addEventListener("click", async () => {
  setStatus("Creating rewrite draft...");
  const formData = new FormData(form);
  const response = await fetch("/resume/rewrite", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    setStatus("Rewrite failed");
    return;
  }

  const blob = await response.blob();
  const disposition = response.headers.get("content-disposition") || "";
  const match = disposition.match(/filename="([^"]+)"/);
  const filename = match ? match[1] : "targeted_resume_rewrite.txt";
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  setStatus("Rewrite draft downloaded");
});
