document.addEventListener("DOMContentLoaded", () => {
    // Current user state
    let currentUser = null;
    let autoUpdateInterval = null;

    // Chart references
    let chartEnergy = null;
    let chartWater = null;
    let chartClimate = null;

    // DOM Elements
    const tabTriggers = document.querySelectorAll(".sidebar-menu li");
    const tabPanels = document.querySelectorAll(".tab-panel");
    const btnExportPdf = document.getElementById("btn-export-pdf");
    const btnToggleFullscreen = document.getElementById("btn-toggle-fullscreen");
    const btnMobileToggle = document.getElementById("btn-mobile-toggle");
    const sidebar = document.querySelector(".sidebar");
    const sidebarOverlay = document.getElementById("sidebar-overlay");
    const currentTimeVal = document.getElementById("current-time-val");
    const loginTriggerBtn = document.getElementById("login-trigger-btn");
    const loginModal = document.getElementById("login-modal");
    const loginModalClose = document.getElementById("login-modal-close");
    const loginCancelBtn = document.getElementById("login-cancel-btn");
    const loginForm = document.getElementById("login-form");
    const loginErrorMsg = document.getElementById("login-error-msg");
    const profileName = document.getElementById("profile-name");
    const profileRole = document.getElementById("profile-role");

    // Circular Score SVGs
    const buildingScoreCircle = document.getElementById("building-score-circle");
    const valBuildingScore = document.getElementById("val-building-score");
    const valBuildingGrade = document.getElementById("val-building-grade");

    // Metric Displays
    const valEnergy = document.getElementById("val-energy");
    const scoreEnergy = document.getElementById("score-energy");
    const valWater = document.getElementById("val-water");
    const scoreWater = document.getElementById("score-water");
    const valTemp = document.getElementById("val-temp");
    const scoreClimate = document.getElementById("score-climate");
    const valCarbon = document.getElementById("val-carbon");
    const valHumidity = document.getElementById("val-humidity");
    const badgeAlertsCount = document.getElementById("badge-alerts-count");
    const activeAlertsTag = document.getElementById("active-alerts-tag");
    const modeIndicatorPill = document.getElementById("mode-indicator-pill");
    const modeText = document.getElementById("mode-text");

    // CSV elements
    const csvDropzone = document.getElementById("csv-dropzone");
    const csvFileInput = document.getElementById("csv-file-input");
    const csvFileName = document.getElementById("csv-file-name");
    const btnSubmitCsv = document.getElementById("btn-submit-csv");

    // Settings elements
    const settingsAuthOverlay = document.getElementById("settings-auth-overlay");
    const btnSettingsUnlock = document.getElementById("btn-settings-unlock");
    const btnSaveSettings = document.getElementById("btn-save-settings");

    // Set real-time clock
    function updateClock() {
        const now = new Date();
        currentTimeVal.textContent = now.toLocaleString();
    }
    setInterval(updateClock, 1000);
    updateClock();

    // --- FULLSCREEN TOGGLE SYSTEM ---
    if (btnToggleFullscreen) {
        btnToggleFullscreen.addEventListener("click", () => {
            if (!document.fullscreenElement) {
                if (document.documentElement.requestFullscreen) {
                    document.documentElement.requestFullscreen().catch(err => {
                        console.warn("Fullscreen request error:", err);
                    });
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
            }
        });

        document.addEventListener("fullscreenchange", () => {
            const icon = btnToggleFullscreen.querySelector("i");
            const span = btnToggleFullscreen.querySelector("span");
            if (document.fullscreenElement) {
                if (icon) icon.className = "fa-solid fa-compress";
                if (span) span.textContent = "Exit Fullscreen";
            } else {
                if (icon) icon.className = "fa-solid fa-expand";
                if (span) span.textContent = "Fullscreen";
            }
            setTimeout(resizeAllCharts, 200);
        });
    }

    // --- MOBILE SIDEBAR DRAWER SYSTEM ---
    if (btnMobileToggle && sidebar && sidebarOverlay) {
        btnMobileToggle.addEventListener("click", () => {
            sidebar.classList.toggle("open");
            sidebarOverlay.classList.toggle("active");
        });
        sidebarOverlay.addEventListener("click", () => {
            sidebar.classList.remove("open");
            sidebarOverlay.classList.remove("active");
        });
    }

    function resizeAllCharts() {
        if (chartEnergy) chartEnergy.resize();
        if (chartWater) chartWater.resize();
        if (chartClimate) chartClimate.resize();
    }
    window.addEventListener("resize", () => {
        resizeAllCharts();
    });

    // --- TAB NAVIGATION SYSTEM ---
    tabTriggers.forEach(trigger => {
        trigger.addEventListener("click", () => {
            const targetTab = trigger.getAttribute("data-tab");

            // Close mobile sidebar on tab selection
            if (window.innerWidth <= 1024 && sidebar && sidebarOverlay) {
                sidebar.classList.remove("open");
                sidebarOverlay.classList.remove("active");
            }

            // Update active menu item
            tabTriggers.forEach(t => t.classList.remove("active"));
            trigger.classList.add("active");

            // Update active content panel
            tabPanels.forEach(p => {
                p.classList.remove("active");
                if (p.getAttribute("id") === `tab-${targetTab}`) {
                    p.classList.add("active");
                }
            });

            // Adjust page title
            const titleMap = {
                dashboard: "Ecological Analytics",
                alerts: "Live System Alerts",
                upload: "CSV Audit Ingestion",
                leed: "LEED Design Certifier",
                logs: "Database Logs Explorer",
                settings: "Configuration Panels",
                about: "System Architecture"
            };
            document.getElementById("page-title").textContent = titleMap[targetTab] || "EcoBuild Dashboard";

            // If entering dashboard, refresh charts
            if (targetTab === "dashboard") {
                fetchStats();
                fetchCharts();
                setTimeout(resizeAllCharts, 150);
            } else if (targetTab === "alerts") {
                fetchAlerts();
            } else if (targetTab === "settings") {
                fetchSettings();
            } else if (targetTab === "logs") {
                fetchLogs();
            }
        });
    });

    // --- CHART.JS INITIALIZATION ---
    function initCharts() {
        const fontConfig = {
            family: "'Inter', sans-serif",
            size: 11,
            color: "#475569"
        };

        // 1. Energy Line Chart
        const ctxEnergy = document.getElementById("chart-energy").getContext("2d");
        chartEnergy = new Chart(ctxEnergy, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Power load (W)',
                    data: [],
                    borderColor: '#d97706',
                    backgroundColor: 'rgba(217, 119, 6, 0.06)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.35,
                    pointRadius: 3,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } },
                    y: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } }
                }
            }
        });

        // 2. Water Flow Chart
        const ctxWater = document.getElementById("chart-water").getContext("2d");
        chartWater = new Chart(ctxWater, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Flow rate (L/min)',
                    data: [],
                    borderColor: '#0891b2',
                    backgroundColor: 'rgba(8, 145, 178, 0.06)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.35,
                    pointRadius: 3,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } },
                    y: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } }
                }
            }
        });

        // 3. Thermal Comfort Double-Axis Line Chart
        const ctxClimate = document.getElementById("chart-climate").getContext("2d");
        chartClimate = new Chart(ctxClimate, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Temperature (°C)',
                        data: [],
                        borderColor: '#7c3aed',
                        backgroundColor: 'transparent',
                        borderWidth: 2.5,
                        tension: 0.35,
                        yAxisID: 'yTemp',
                        pointRadius: 3
                    },
                    {
                        label: 'Humidity (%)',
                        data: [],
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.04)',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: true,
                        tension: 0.35,
                        yAxisID: 'yHumidity',
                        pointRadius: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: { color: '#475569', font: fontConfig, boxWidth: 12 }
                    }
                },
                scales: {
                    x: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } },
                    yTemp: {
                        type: 'linear',
                        position: 'left',
                        grid: { color: 'rgba(0, 0, 0, 0.04)' },
                        ticks: { color: '#7c3aed', font: fontConfig }
                    },
                    yHumidity: {
                        type: 'linear',
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        ticks: { color: '#059669', font: fontConfig }
                    }
                }
            }
        });
    }

    // --- GAUGES AND SCORES UPDATE ---
    function setBuildingScore(score) {
        valBuildingScore.textContent = Math.round(score);
        const circumference = 2 * Math.PI * 70; // 439.82
        const offset = circumference - (score / 100) * circumference;
        buildingScoreCircle.style.strokeDashoffset = offset;

        // Set grade color and text
        if (score >= 80) {
            valBuildingGrade.textContent = "Platinum Rating (Exceptional)";
            valBuildingGrade.style.color = "var(--neon-green)";
            buildingScoreCircle.style.stroke = "var(--neon-green)";
        } else if (score >= 65) {
            valBuildingGrade.textContent = "Gold Rating (High Efficiency)";
            valBuildingGrade.style.color = "var(--neon-cyan)";
            buildingScoreCircle.style.stroke = "var(--neon-cyan)";
        } else if (score >= 50) {
            valBuildingGrade.textContent = "Silver Rating (Moderate)";
            valBuildingGrade.style.color = "var(--neon-amber)";
            buildingScoreCircle.style.stroke = "var(--neon-amber)";
        } else {
            valBuildingGrade.textContent = "Certified Baseline (Action Required)";
            valBuildingGrade.style.color = "var(--neon-red)";
            buildingScoreCircle.style.stroke = "var(--neon-red)";
        }
    }

    // --- DATA FETCHING & API INTERFACES ---
    async function fetchStats() {
        try {
            const res = await fetch('/api/stats');
            if (!res.ok) return;
            const data = await res.json();

            // Render Real-time metrics
            valEnergy.textContent = data.energy.value.toFixed(1);
            scoreEnergy.textContent = `${data.energy.score}/100`;

            valWater.textContent = data.water.value.toFixed(1);
            scoreWater.textContent = `${data.water.score}/100`;

            valTemp.textContent = data.climate.temp.toFixed(1);
            scoreClimate.textContent = `${data.climate.score}/100`;
            valHumidity.textContent = `${data.climate.humidity.toFixed(1)}%`;

            // Carbon emissions calculated: standard coefficient 0.82 kg CO2 / kWh
            const carbonKg = ((data.energy.value / 1000) * 0.82).toFixed(2);
            valCarbon.textContent = carbonKg;

            // Trees saved
            const treesEq = (carbonKg * 0.05).toFixed(1);
            const valTreesEl = document.getElementById("val-trees");
            if (valTreesEl) valTreesEl.textContent = treesEq;

            // Sustainability Goals Update
            const energyLimit = 3500;
            const energyPct = Math.min(100, Math.round((data.energy.value / energyLimit) * 100));
            const energyGoalProg = document.getElementById("energy-goal-progress");
            if (energyGoalProg) {
                energyGoalProg.style.width = `${energyPct}%`;
                energyGoalProg.style.background = energyPct > 90 ? 'var(--neon-red)' : (energyPct > 75 ? 'var(--neon-amber)' : 'var(--neon-green)');
            }
            const energyGoalCurr = document.getElementById("energy-goal-curr");
            if (energyGoalCurr) energyGoalCurr.textContent = `${data.energy.value.toFixed(0)} W`;
            const energyGoalPctEl = document.getElementById("energy-goal-pct");
            if (energyGoalPctEl) energyGoalPctEl.textContent = `${energyPct}% used`;

            const waterLimit = 25;
            const waterPct = Math.min(100, Math.round((data.water.value / waterLimit) * 100));
            const waterGoalProg = document.getElementById("water-goal-progress");
            if (waterGoalProg) {
                waterGoalProg.style.width = `${waterPct}%`;
                waterGoalProg.style.background = waterPct > 90 ? 'var(--neon-red)' : 'var(--neon-cyan)';
            }
            const waterGoalCurr = document.getElementById("water-goal-curr");
            if (waterGoalCurr) waterGoalCurr.textContent = `${data.water.value.toFixed(1)} L/m`;
            const waterGoalPctEl = document.getElementById("water-goal-pct");
            if (waterGoalPctEl) waterGoalPctEl.textContent = `${waterPct}% used`;

            // Overall Score
            setBuildingScore(data.building_score);

            // Anomaly Badge Count
            badgeAlertsCount.textContent = data.active_anomalies_count;
            if (data.active_anomalies_count > 0) {
                badgeAlertsCount.style.display = "inline-block";
            } else {
                badgeAlertsCount.style.display = "none";
            }
        } catch (err) {
            console.warn("Telemetry fetch stats error:", err);
        }
    }

    async function fetchCharts() {
        try {
            const res = await fetch('/api/charts');
            if (!res.ok) return;
            const data = await res.json();

            // Update Chart datasets
            if (chartEnergy) {
                chartEnergy.data.labels = data.energy.labels;
                chartEnergy.data.datasets[0].data = data.energy.values;
                chartEnergy.update();
            }

            if (chartWater) {
                chartWater.data.labels = data.water.labels;
                chartWater.data.datasets[0].data = data.water.values;
                chartWater.update();
            }

            if (chartClimate) {
                chartClimate.data.labels = data.climate.labels;
                chartClimate.data.datasets[0].data = data.climate.temp;
                chartClimate.data.datasets[1].data = data.climate.humidity;
                chartClimate.update();
            }
        } catch (err) {
            console.warn("Telemetry fetch charts error:", err);
        }
    }

    async function fetchAlerts() {
        try {
            const res = await fetch('/api/alerts');
            if (!res.ok) return;
            const data = await res.json();

            const tbody = document.getElementById("alerts-tbody");
            activeAlertsTag.textContent = `${data.length} Active Anomalies`;

            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" class="text-center">No anomalies registered. Systems functioning normally.</td></tr>`;
                return;
            }

            tbody.innerHTML = data.map(item => `
                <tr>
                    <td><span class="badge-outline-danger">${item.severity}</span></td>
                    <td><strong>${item.node_id}</strong></td>
                    <td>${item.value}</td>
                    <td>${item.threshold}</td>
                    <td>${item.timestamp}</td>
                    <td><span class="badge-outline-danger">Triggered</span></td>
                    <td>
                        <button class="action-link-btn" onclick="dismissAlert(${item.id})">Acknowledge</button>
                    </td>
                </tr>
            `).join("");
        } catch (err) {
            console.warn("Alerts fetch error:", err);
        }
    }

    window.dismissAlert = async function(id) {
        try {
            await fetch(`/api/alerts/${id}/dismiss`, { method: 'POST' });
            fetchAlerts();
            fetchStats();
        } catch (err) {
            console.error("Failed to dismiss alert:", err);
        }
    };

    async function fetchLogs() {
        try {
            const res = await fetch('/api/logs');
            if (!res.ok) return;
            const data = await res.json();

            const tbody = document.getElementById("logs-tbody");
            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="text-center">No persistent records found.</td></tr>`;
                return;
            }

            tbody.innerHTML = data.map(row => `
                <tr>
                    <td>#${row.id}</td>
                    <td><strong>${row.node_id}</strong></td>
                    <td>${row.value1 != null ? row.value1 : '-'}</td>
                    <td>${row.value2 != null ? row.value2 : '-'}</td>
                    <td><span class="badge-outline-success">${row.score != null ? row.score : '-'}</span></td>
                    <td>${row.timestamp}</td>
                </tr>
            `).join("");
        } catch (err) {
            console.warn("Logs fetch error:", err);
        }
    }

    const btnRefreshLogs = document.getElementById("btn-refresh-logs");
    if (btnRefreshLogs) {
        btnRefreshLogs.addEventListener("click", fetchLogs);
    }

    // --- LEED SCORING SYSTEM ---
    const leedCheckboxes = document.querySelectorAll(".leed-checkbox");
    const valLeedGrade = document.getElementById("val-leed-grade");

    function calculateLeedScore() {
        let total = 0;
        leedCheckboxes.forEach(cb => {
            if (cb.checked) total += parseInt(cb.value);
        });

        let grade = "Certified";
        if (total >= 80) grade = "LEED Platinum Rating";
        else if (total >= 60) grade = "LEED Gold Rating";
        else if (total >= 50) grade = "LEED Silver Rating";
        else if (total >= 40) grade = "LEED Certified Standard";
        else grade = "Targeting Certification";

        valLeedGrade.textContent = `${grade} (${total} Points)`;
    }

    leedCheckboxes.forEach(cb => {
        cb.addEventListener("change", calculateLeedScore);
    });

    // --- CSV UPLOAD INGESTION ---
    if (csvDropzone) {
        csvDropzone.addEventListener("click", () => csvFileInput.click());
        csvDropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            csvDropzone.classList.add("dragover");
        });
        csvDropzone.addEventListener("dragleave", () => csvDropzone.classList.remove("dragover"));
        csvDropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            csvDropzone.classList.remove("dragover");
            if (e.dataTransfer.files.length) {
                csvFileInput.files = e.dataTransfer.files;
                handleSelectedFile();
            }
        });

        csvFileInput.addEventListener("change", handleSelectedFile);
    }

    function handleSelectedFile() {
        if (csvFileInput.files.length > 0) {
            csvFileName.textContent = csvFileInput.files[0].name;
            csvDropzone.classList.add("has-file");
            btnSubmitCsv.removeAttribute("disabled");
        }
    }

    if (btnSubmitCsv) {
        btnSubmitCsv.addEventListener("click", async () => {
            if (!csvFileInput.files.length) return;
            const formData = new FormData();
            formData.append("file", csvFileInput.files[0]);

            btnSubmitCsv.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Ingesting dataset...`;
            btnSubmitCsv.setAttribute("disabled", "true");

            try {
                const res = await fetch('/api/demo/upload', {
                    method: 'POST',
                    body: formData
                });
                const result = await res.json();
                alert(result.message || "CSV ingested successfully!");
                csvFileName.textContent = "No file selected";
                csvDropzone.classList.remove("has-file");
                csvFileInput.value = "";
                fetchStats();
            } catch (err) {
                alert("Failed to process CSV file.");
            } finally {
                btnSubmitCsv.innerHTML = `<i class="fa-solid fa-square-check"></i> <span>Start CSV Ingestion Process</span>`;
            }
        });
    }

    // --- AUTHENTICATION & LOGIN ---
    function openLoginModal() {
        loginModal.style.display = "flex";
    }

    function closeLoginModal() {
        loginModal.style.display = "none";
        loginErrorMsg.style.display = "none";
    }

    loginTriggerBtn.addEventListener("click", () => {
        if (currentUser) {
            // Logout
            currentUser = null;
            profileName.textContent = "Guest View";
            profileRole.textContent = "Limited Access";
            loginTriggerBtn.innerHTML = `<i class="fa-solid fa-right-to-bracket"></i>`;
            settingsAuthOverlay.style.display = "flex";
        } else {
            openLoginModal();
        }
    });

    loginModalClose.addEventListener("click", closeLoginModal);
    loginCancelBtn.addEventListener("click", closeLoginModal);

    btnSettingsUnlock.addEventListener("click", openLoginModal);

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const u = document.getElementById("login-username").value;
        const p = document.getElementById("login-password").value;

        try {
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: u, password: p })
            });
            const data = await res.json();

            if (res.ok && data.success) {
                currentUser = data.user;
                profileName.textContent = data.user.name;
                profileRole.textContent = data.user.role;
                loginTriggerBtn.innerHTML = `<i class="fa-solid fa-right-from-bracket" style="color: var(--neon-red);"></i>`;
                settingsAuthOverlay.style.display = "none";
                closeLoginModal();
                fetchSettings();
            } else {
                loginErrorMsg.style.display = "block";
            }
        } catch (err) {
            loginErrorMsg.style.display = "block";
        }
    });

    // --- SETTINGS FETCH & SAVE ---
    async function fetchSettings() {
        try {
            const res = await fetch('/api/settings');
            if (!res.ok) return;
            const data = await res.json();

            // Set system mode
            if (data.mode === 'live') {
                document.getElementById("mode-live").checked = true;
                modeIndicatorPill.classList.remove("demo-mode");
                modeText.textContent = "LIVE IoT MODE";
            } else {
                document.getElementById("mode-demo").checked = true;
                modeIndicatorPill.classList.add("demo-mode");
                modeText.textContent = "DEMO SIMULATION";
            }

            // Set Sensor Thresholds
            if (data.nodes) {
                if (data.nodes.node_energy) {
                    document.getElementById("input-thresh-energy").value = data.nodes.node_energy.threshold;
                    document.getElementById("input-cal-energy").value = data.nodes.node_energy.calibration_factor;
                }
                if (data.nodes.node_water) {
                    document.getElementById("input-thresh-water").value = data.nodes.node_water.threshold;
                    document.getElementById("input-cal-water").value = data.nodes.node_water.calibration_factor;
                }
                if (data.nodes.node_climate) {
                    document.getElementById("input-thresh-climate").value = data.nodes.node_climate.threshold;
                    document.getElementById("input-cal-climate").value = data.nodes.node_climate.calibration_factor;
                }
            }
        } catch (err) {
            console.warn("Failed to fetch settings:", err);
        }
    }

    if (btnSaveSettings) {
        btnSaveSettings.addEventListener("click", async () => {
            const selectedMode = document.querySelector('input[name="system-mode"]:checked').value;
            const settingsPayload = {
                mode: selectedMode,
                nodes: {
                    node_energy: {
                        threshold: parseFloat(document.getElementById("input-thresh-energy").value),
                        calibration_factor: parseFloat(document.getElementById("input-cal-energy").value)
                    },
                    node_water: {
                        threshold: parseFloat(document.getElementById("input-thresh-water").value),
                        calibration_factor: parseFloat(document.getElementById("input-cal-water").value)
                    },
                    node_climate: {
                        threshold: parseFloat(document.getElementById("input-thresh-climate").value),
                        calibration_factor: parseFloat(document.getElementById("input-cal-climate").value)
                    }
                }
            };

            try {
                const res = await fetch('/api/settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(settingsPayload)
                });
                if (res.ok) {
                    alert("System configuration and calibration saved successfully!");
                    fetchSettings();
                } else {
                    alert("Failed to save settings. Admin authentication required.");
                }
            } catch (err) {
                alert("Error connecting to server.");
            }
        });
    }

    // --- PDF EXPORT FEATURE ---
    if (btnExportPdf) {
        btnExportPdf.addEventListener("click", () => {
            const element = document.getElementById('printable-area');
            const opt = {
                margin: 0.3,
                filename: `EcoBuild_Report_${new Date().toISOString().slice(0,10)}.pdf`,
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
            };
            html2pdf().set(opt).from(element).save();
        });
    }

    // --- INITIALIZE & START LOOP ---
    initCharts();
    fetchStats();
    fetchCharts();

    // Auto-refresh stats every 2.5 seconds
    autoUpdateInterval = setInterval(() => {
        fetchStats();
    }, 2500);

    // Auto-refresh charts every 5 seconds
    setInterval(() => {
        fetchCharts();
    }, 5000);
});