
let incidents = [
    {
        id: "INC-1001",
        title: "Production API outage",
        severity: "CRITICAL",
        status: "OPEN",
        date: "2026-11-15"
    },
    {
        id: "INC-1002",
        title: "Database response degraded",
        severity: "HIGH",
        status: "IN PROGRESS",
        date: "2026-11-15"
    },
    {
        id: "INC-1003",
        title: "Intermittent login issue",
        severity: "LOW",
        status: "RESOLVED",
        date: "2026-11-14"
    }
];

const table = document.getElementById("incidentTable");
const modal = document.getElementById("incidentModal");

function renderIncidents() {
    document.getElementById("totalCount").textContent = incidents.length;
    document.getElementById("openCount").textContent =
        incidents.filter(i => i.status === "OPEN" || i.status === "IN PROGRESS").length;
    document.getElementById("criticalCount").textContent =
        incidents.filter(i => i.severity === "CRITICAL" && i.status !== "RESOLVED").length;
    document.getElementById("resolvedCount").textContent =
        incidents.filter(i => i.status === "RESOLVED").length;

    document.getElementById("emptyState").hidden = incidents.length > 0;

    table.innerHTML = incidents.map(incident => `
        <tr>
            <td>
                <strong>${escapeHTML(incident.title)}</strong><br>
                <small>${escapeHTML(incident.id)}</small>
            </td>
            <td><span class="badge ${incident.severity}">${incident.severity}</span></td>
            <td><span class="status">${incident.status}</span></td>
            <td>${incident.date}</td>
            <td>
                ${incident.status !== "RESOLVED"
                    ? `<button class="action-btn" data-id="${incident.id}">Resolve</button>`
                    : "—"}
            </td>
        </tr>
    `).join("");
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

document.getElementById("openModal").addEventListener("click", () => {
    modal.classList.add("show");
});

document.getElementById("closeModal").addEventListener("click", () => {
    modal.classList.remove("show");
});

document.getElementById("incidentForm").addEventListener("submit", event => {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();

    if (!title || !description) return;

    const text = description.toLowerCase();

    let severity = "MEDIUM";

    if (["outage", "down", "data loss", "security breach"].some(word => text.includes(word))) {
        severity = "CRITICAL";
    } else if (["major", "degraded", "multiple users"].some(word => text.includes(word))) {
        severity = "HIGH";
    } else if (["minor", "slow", "intermittent"].some(word => text.includes(word))) {
        severity = "LOW";
    }

    incidents.unshift({
        id: "INC-" + Date.now(),
        title,
        severity,
        status: "OPEN",
        date: new Date().toISOString().slice(0, 10)
    });

    event.target.reset();
    modal.classList.remove("show");
    renderIncidents();
});

table.addEventListener("click", event => {
    const button = event.target.closest("[data-id]");
    if (!button) return;

    const incident = incidents.find(i => i.id === button.dataset.id);
    if (incident) {
        incident.status = "RESOLVED";
        renderIncidents();
    }
});

renderIncidents();
