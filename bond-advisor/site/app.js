const money = new Intl.NumberFormat(undefined, { maximumFractionDigits: 0 });

function gp(value) {
  if (typeof value !== "number") return "Unknown";
  return `${money.format(value)} GP`;
}

function text(value, fallback = "—") {
  return value === null || value === undefined || value === "" ? fallback : String(value);
}

function methodCard(item) {
  const card = document.createElement("article");
  card.className = "method-card";
  card.innerHTML = `
    <h3>${text(item.method_name || item.method_id, "Unnamed method")}</h3>
    <div class="meta">
      <span class="badge">Priority ${text(item.priority)}</span>
      <span class="badge">${text(item.confidence, "unknown confidence")}</span>
      <span class="badge">${text(item.time_minutes, "?")} min</span>
      <span class="badge">${gp(item.expected_gp)}</span>
    </div>
    <p>${text(item.reason, "No reason provided.")}</p>
    <p class="muted"><strong>Next:</strong> ${text(item.next_action, "Review manually.")}</p>
  `;
  return card;
}

function avoidItem(item) {
  const li = document.createElement("li");
  li.textContent = `${text(item.method_name || item.method_id, "Unnamed method")}: ${text(item.reason, "No reason provided.")}`;
  return li;
}

async function loadPlan() {
  const response = await fetch("daily_plan.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`Could not load daily_plan.json: ${response.status}`);
  return response.json();
}

async function main() {
  const headline = document.getElementById("headline");
  const recommended = document.getElementById("recommended");
  const avoid = document.getElementById("avoid");
  const notes = document.getElementById("notes");
  const source = document.getElementById("source");
  const target = document.getElementById("target");

  try {
    const plan = await loadPlan();
    source.textContent = text(plan.source, "generated");
    target.textContent = gp(plan.daily_target_gp);
    headline.textContent = text(plan.headline, "No headline provided.");

    recommended.innerHTML = "";
    const recs = plan.recommended_plan || [];
    if (recs.length) {
      recs.forEach(item => recommended.appendChild(methodCard(item)));
    } else {
      recommended.innerHTML = `<p class="muted">No recommendations generated yet.</p>`;
    }

    avoid.innerHTML = "";
    const avoids = plan.avoid_today || [];
    if (avoids.length) {
      const ul = document.createElement("ul");
      avoids.forEach(item => ul.appendChild(avoidItem(item)));
      avoid.appendChild(ul);
    } else {
      avoid.innerHTML = `<p class="muted">No avoid list generated.</p>`;
    }

    notes.innerHTML = "";
    const allNotes = [...(plan.missing_info_needed || []), ...(plan.confidence_notes || [])];
    if (allNotes.length) {
      allNotes.forEach(note => {
        const li = document.createElement("li");
        li.textContent = note;
        notes.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.textContent = "No notes.";
      notes.appendChild(li);
    }
  } catch (error) {
    headline.textContent = error.message;
    source.textContent = "error";
    target.textContent = "Unknown";
  }
}

main();
