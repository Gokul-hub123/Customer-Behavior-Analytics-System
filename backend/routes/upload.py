const API_BASE = "http://localhost:8000";

const elements = {
  dashboardCards: document.getElementById("dashboard-cards"),
  insightsBox: document.getElementById("insights-box"),
  uploadStatus: document.getElementById("uploadStatus"),
  datasetPreview: document.getElementById("datasetPreview"),
  cleaningSummary: document.getElementById("cleaningSummary"),
  analysisCards: document.getElementById("analysisCards"),
  segmentationResult: document.getElementById("segmentationResult"),
  forecastResult: document.getElementById("forecastResult"),
  reportResult: document.getElementById("reportResult"),
};

const charts = {};

function setStatus(element, text, isError = false) {
  element.innerHTML = `<p style="color:${isError ? '#b91c1c' : '#166534'}; font-weight: 600; margin: 0;">${text}</p>`;
}

function renderCards(data) {
  const cards = [
    { label: "Total Customers", value: data.total_customers || 0 },
    { label: "Total Transactions", value: data.total_transactions || 0 },
    { label: "Total Sales", value: `₹${(data.total_sales || 0).toFixed(2)}` },
    { label: "Average Purchase", value: `₹${(data.average_purchase_value || 0).toFixed(2)}` },
  ];

  elements.dashboardCards.innerHTML = cards.map(card => `
    <div class="card">
      <h3>${card.label}</h3>
      <div class="value">${card.value}</div>
    </div>
  `).join("");
}

function renderInsights(data) {
  const insights = data.key_insights || [];
  elements.insightsBox.innerHTML = `
    <h3>Key Insights</h3>
    <ul>${insights.map(i => `<li>${i}</li>`).join("")}</ul>
  `;
}

function buildChartConfig(labels, values, label, color) {
  return {
    type: "line",
    data: {
      labels,
      datasets: [{
        label,
        data: values,
        borderColor: color,
        backgroundColor: color + "22",
        fill: false,
        tension: 0.3,
      }],
    },
    options: { responsive: true, maintainAspectRatio: false },
  };
}

function buildBarChartConfig(labels, values, label, color) {
  return {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label,
        data: values,
        backgroundColor: color,
      }],
    },
    options: { responsive: true, maintainAspectRatio: false },
  };
}

async function loadDashboard() {
  try {
    const response = await fetch(`${API_BASE}/api/dashboard`);
    const data = await response.json();
    renderCards(data);
    renderInsights(data);

    const monthlyLabels = data.monthly_sales?.map(item => item.month || item.date) || [];
    const monthlyValues = data.monthly_sales?.map(item => Number(item.sales || 0)) || [];
    const categoryLabels = data.category_sales?.map(item => item.category || "General") || [];
    const categoryValues = data.category_sales?.map(item => Number(item.sales || 0)) || [];
    const productLabels = data.top_products?.map(item => item.product_name || "Product") || [];
    const productValues = data.top_products?.map(item => Number(item.sales || 0)) || [];
    const distributionLabels = data.customer_distribution?.map(item => item.range || "Range") || [];
    const distributionValues = data.customer_distribution?.map(item => Number(item.customers || 0)) || [];

    if (charts.monthlySales) charts.monthlySales.destroy();
    if (charts.categorySales) charts.categorySales.destroy();
    if (charts.topProducts) charts.topProducts.destroy();
    if (charts.customerDistribution) charts.customerDistribution.destroy();

    charts.monthlySales = new Chart(document.getElementById("monthlySalesChart"), buildChartConfig(monthlyLabels, monthlyValues, "Monthly Sales", "#2563eb"));
    charts.categorySales = new Chart(document.getElementById("categorySalesChart"), buildBarChartConfig(categoryLabels, categoryValues, "Sales by Category", "#10b981"));
    charts.topProducts = new Chart(document.getElementById("topProductsChart"), buildBarChartConfig(productLabels, productValues, "Top Products", "#f59e0b"));
    charts.customerDistribution = new Chart(document.getElementById("customerDistributionChart"), buildBarChartConfig(distributionLabels, distributionValues, "Customer Purchase Distribution", "#a78bfa"));
  } catch (error) {
    setStatus(elements.uploadStatus, "Unable to load dashboard data.", true);
  }
}

function formatTable(rows) {
  if (!rows || !rows.length) return "<p>No data available.</p>";
  const columns = Object.keys(rows[0]);
  return `
    <table>
      <thead>
        <tr>${columns.map(col => `<th>${col}</th>`).join("")}</tr>
      </thead>
      <tbody>
        ${rows.slice(0, 10).map(row => `<tr>${columns.map(col => `<td>${row[col]}</td>`).join("")}</tr>`).join("")}
      </tbody>
    </table>
  `;
}

document.getElementById("uploadForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const fileInput = document.getElementById("csvFile");
  const file = fileInput.files[0];
  if (!file) {
    setStatus(elements.uploadStatus, "Please choose a CSV file first.", true);
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_BASE}/api/upload`, { method: "POST", body: formData });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Upload failed.");
    }
    setStatus(elements.uploadStatus, data.message || "Dataset uploaded successfully");
    elements.datasetPreview.innerHTML = formatTable(data.preview || []);
    await loadDashboard();
  } catch (error) {
    setStatus(elements.uploadStatus, error.message, true);
  }
});

document.getElementById("cleanBtn").addEventListener("click", async () => {
  try {
    const response = await fetch(`${API_BASE}/api/clean`, { method: "POST" });
    const data = await response.json();
    elements.cleaningSummary.innerHTML = `<h3>Cleaning Results</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
  } catch (error) {
    elements.cleaningSummary.innerHTML = `<p style="color:#b91c1c">Cleaning failed.</p>`;
  }
});

async function loadAnalysis() {
  try {
    const response = await fetch(`${API_BASE}/api/analysis`);
    const data = await response.json();

    const cards = [
      { label: "Total Sales", value: `₹${(data.total_sales || 0).toFixed(2)}` },
      { label: "Average Sales", value: `₹${(data.average_sales || 0).toFixed(2)}` },
      { label: "Min Sale", value: `₹${(data.minimum_sale || 0).toFixed(2)}` },
      { label: "Max Sale", value: `₹${(data.maximum_sale || 0).toFixed(2)}` },
      { label: "Total Customers", value: data.total_customers || 0 },
      { label: "Total Transactions", value: data.total_transactions || 0 },
    ];

    elements.analysisCards.innerHTML = cards.map(card => `
      <div class="card">
        <h3>${card.label}</h3>
        <div class="value">${card.value}</div>
      </div>
    `).join("");

    const monthlyLabels = data.monthly_sales?.map(item => item.month || item.date) || [];
    const monthlyValues = data.monthly_sales?.map(item => Number(item.sales || 0)) || [];
    const categoryLabels = data.top_categories?.map(item => item.category || "General") || [];
    const categoryValues = data.top_categories?.map(item => Number(item.sales || 0)) || [];

    if (charts.analysisMonthly) charts.analysisMonthly.destroy();
    if (charts.analysisCategory) charts.analysisCategory.destroy();

    charts.analysisMonthly = new Chart(document.getElementById("analysisMonthlyChart"), buildChartConfig(monthlyLabels, monthlyValues, "Monthly Sales", "#2563eb"));
    charts.analysisCategory = new Chart(document.getElementById("analysisCategoryChart"), buildBarChartConfig(categoryLabels, categoryValues, "Category Sales", "#ef4444"));
  } catch (error) {
    elements.analysisCards.innerHTML = "<p>Failed to load analysis.</p>";
  }
}

document.getElementById("analysisBtn").addEventListener("click", loadAnalysis);

document.getElementById("segmentationBtn").addEventListener("click", async () => {
  try {
    const response = await fetch(`${API_BASE}/api/segmentation`, { method: "POST" });
    const data = await response.json();
    elements.segmentationResult.innerHTML = `<h3>Customer Segmentation</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
  } catch (error) {
    elements.segmentationResult.innerHTML = "<p>Segmentation failed.</p>";
  }
});

document.getElementById("forecastBtn").addEventListener("click", async () => {
  try {
    const response = await fetch(`${API_BASE}/api/forecast`, { method: "POST" });
    const data = await response.json();
    elements.forecastResult.innerHTML = `<h3>Forecast Results</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;

    const historical = data.historical_sales || [];
    const forecast = data.forecast_table || [];
    const labels = [...historical.map(item => item.date), ...forecast.map(item => item.forecast_month)];
    const values = [...historical.map(item => Number(item.sales || 0)), ...forecast.map(item => Number(item.predicted_sales || 0))];

    if (charts.forecastChart) charts.forecastChart.destroy();
    charts.forecastChart = new Chart(document.getElementById("forecastChart"), {
      type: "line",
      data: {
        labels,
        datasets: [
          { label: "Actual Sales", data: historical.map(item => Number(item.sales || 0)), borderColor: "#1d4ed8", backgroundColor: "#93c5fd", fill: false },
          { label: "Forecast Sales", data: [...Array(historical.length).fill(null), ...forecast.map(item => Number(item.predicted_sales || 0))], borderColor: "#ef4444", backgroundColor: "#fca5a5", fill: false },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false },
    });
  } catch (error) {
    elements.forecastResult.innerHTML = "<p>Forecast generation failed.</p>";
  }
});

document.getElementById("reportBtn").addEventListener("click", async () => {
  try {
    const response = await fetch(`${API_BASE}/api/report`);
    const data = await response.json();
    elements.reportResult.innerHTML = `<h3>Report Summary</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
  } catch (error) {
    elements.reportResult.innerHTML = "<p>Report generation failed.</p>";
  }
});

document.querySelectorAll(".nav-btn").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(panel => panel.classList.remove("active"));
    button.classList.add("active");
    document.getElementById(button.dataset.target).classList.add("active");
  });
});

loadDashboard();
