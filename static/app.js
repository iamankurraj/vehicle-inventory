const INV = "http://127.0.0.1:8000/inventory";
const RES = "http://127.0.0.1:8000/reserve";
const CHAT_API = "http://127.0.0.1:8000/chat";

let currentVin = null;
let chatSessionId = null;

/* ================= ERROR HELPERS ================= */

function showError(msg) {
  document.getElementById("error").textContent = msg;
}

function clearError() {
  showError("");
}

/* ================= CHAT ================= */

function toggleChat() {
  document.getElementById("chatbot").classList.toggle("minimized");
}

async function sendChat() {
  const input = document.getElementById("chat-text");
  const msg = input.value.trim();
  if (!msg) return;

  const box = document.getElementById("chat-messages");
  box.innerHTML += `<div class="msg user">${msg}</div>`;
  input.value = "";

  const res = await fetch(CHAT_API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg, session_id: chatSessionId })
  });

  const data = await res.json();
  chatSessionId = data.session_id;
  box.innerHTML += `<div class="msg bot">${data.reply}</div>`;
  box.scrollTop = box.scrollHeight;
}

/* ================= VIN ================= */

function openVinModal() {
  document.getElementById("vin-modal").style.display = "block";
}

function closeVinModal() {
  document.getElementById("vin-modal").style.display = "none";
}

async function saveVin() {
  const vin = document.getElementById("vin-input").value.trim();
  const vinError = document.getElementById("vin-error");

  if (!/^[A-Za-z0-9]{17}$/.test(vin)) {
    vinError.textContent = "VIN must be 17 characters.";
    return;
  }

  const res = await fetch(`${RES}/verify-vin?vin=${vin}`);
  const data = await res.json();

  if (!data.valid) {
    vinError.textContent = "VIN not recognized.";
    return;
  }

  currentVin = vin;
  localStorage.setItem("vin", vin);
  document.getElementById("vin-status").textContent = `VIN: ${vin}`;
  closeVinModal();
}

/* ================= DROPDOWNS ================= */

async function loadCountries() {
  const country = document.getElementById("country");
  const res = await fetch(`${INV}/countries`);
  const data = await res.json();

  country.innerHTML = `<option value="">Country</option>`;
  data.forEach(c => country.innerHTML += `<option>${c}</option>`);
}

async function loadRegions() {
  const country = document.getElementById("country");
  const region = document.getElementById("region");

  region.innerHTML = `<option value="">Region</option>`;
  if (!country.value) return;

  const res = await fetch(`${INV}/regions?country=${country.value}`);
  const data = await res.json();
  data.forEach(r => region.innerHTML += `<option>${r}</option>`);
}

async function loadParts() {
  const part = document.getElementById("part");
  const res = await fetch(`${INV}/parts`);
  const data = await res.json();

  part.innerHTML = `<option value="">Part</option>`;
  data.forEach(p => part.innerHTML += `<option>${p}</option>`);
}

/* ================= SEARCH ================= */

async function search() {
  clearError();

  const country = document.getElementById("country").value;
  const region = document.getElementById("region").value;
  const part = document.getElementById("part").value;

  if (!country || !region || !part) {
    showError("Select country, region, and part.");
    return;
  }

  const res = await fetch(
    `${INV}/search?country=${country}&region=${region}&part=${part}`
  );
  const data = await res.json();

  const results = document.getElementById("results");
  results.innerHTML = "";

  data.forEach(x => {
    results.innerHTML += `
      <div class="card">
        <h4>${x.part}</h4>
        <p><b>Provider:</b> ${x.provider}</p>
        <p><b>Available:</b> ${x.quantity}</p>
        <button onclick="reserve('${x.provider}','${x.part}')">Reserve</button>
      </div>
    `;
  });
}

/* ================= RESERVE ================= */

async function reserve(provider, part) {
  if (!currentVin) {
  closeQuickView();   // close product overview
  openVinModal();     // then ask for VIN
  return;
}


  await fetch(
    `${RES}?vin=${currentVin}&provider=${provider}&part=${part}`,
    { method: "POST" }
  );

  search();
}

/* ================= QUICK VIEW ================= */

let qvInventory = [];
let qvPartName = "";

async function openQuickView(partName) {
  qvPartName = partName;

  const res = await fetch(
    `${INV}/part-detail?part_name=${encodeURIComponent(partName)}`
  );
  const data = await res.json();
  qvInventory = data.inventory;

  document.getElementById("qv-part-name").textContent = partName;
  document.getElementById("quick-view").style.display = "block";

  populateQVRegions();
}

function closeQuickView() {
  document.getElementById("quick-view").style.display = "none";
}

function populateQVRegions() {
  const regionSel = document.getElementById("qv-region");
  const regions = [...new Set(qvInventory.map(i => i.region))];

  regionSel.innerHTML = "";
  regions.forEach(r => {
    regionSel.innerHTML += `<option value="${r}">${r}</option>`;
  });

  // 🔥 IMPORTANT: bind change handler
  regionSel.onchange = populateQVProviders;

  populateQVProviders(); // initial load
}

function populateQVProviders() {
  const region = document.getElementById("qv-region").value;
  const providerSel = document.getElementById("qv-provider");

  providerSel.innerHTML = "";

  qvInventory
    .filter(i => i.region === region)
    .forEach(i => {
      providerSel.innerHTML += `
        <option value="${i.provider}" data-qty="${i.quantity}">
          ${i.provider}
        </option>
      `;
    });

  // 🔥 IMPORTANT: bind change handler
  providerSel.onchange = updateQVQty;

  updateQVQty(); // refresh quantity immediately
}

function updateQVQty() {
  const providerSel = document.getElementById("qv-provider");
  if (!providerSel || providerSel.selectedIndex < 0) {
    document.getElementById("qv-qty").textContent = "";
    return;
  }

  const qty = providerSel.options[providerSel.selectedIndex].dataset.qty;
  document.getElementById("qv-qty").textContent =
    `Available quantity: ${qty}`;
}

async function reserveFromQuickView() {
  const provider = document.getElementById("qv-provider").value;

  const res = await fetch(
    `${RES}?vin=${currentVin}&provider=${provider}&part=${qvPartName}`,
    { method: "POST" }
  );

  const data = await res.json();

  if (!res.ok) {
    document.getElementById("qv-error").textContent =
      data.detail || "Reservation failed.";
    return;
  }

  // ✅ close quick view
  closeQuickView();

  // ✅ refresh grid so quantities update
  loadAvailableParts();

  // ✅ clear success feedback
  alert("Part reserved successfully.");
}


/* ================= PARTS GRID ================= */
async function loadAvailableParts() {
  const res = await fetch(`${INV}/available-parts`);
  const data = await res.json();

  const grid = document.getElementById("partsGrid");

  grid.innerHTML = data.map(p => {
    const qty = p.total_quantity;

    const subtitle =
      qty < 3
        ? `Only ${qty} left`
        : "High-performance component engineered for durability and precision.";

    return `
      <div class="product-card"
           onclick="openQuickView('${p.part_name.replace(/'/g, "\\'")}')">

        <div class="product-image">
          <div class="image-placeholder"></div>
        </div>

        <div class="product-info">
          <h4>${p.part_name}</h4>
          <p>${subtitle}</p>
          <span class="view-link">Quick view</span>
        </div>

      </div>
    `;
  }).join("");
}


/* ================= INIT ================= */

document.addEventListener("DOMContentLoaded", () => {
  currentVin = localStorage.getItem("vin");
  if (currentVin) {
    document.getElementById("vin-status").textContent = `VIN: ${currentVin}`;
  }

  document.getElementById("country").addEventListener("change", loadRegions);

  loadCountries();
  loadParts();
  loadAvailableParts();
});
