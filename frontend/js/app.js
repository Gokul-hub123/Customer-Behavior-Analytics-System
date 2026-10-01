* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #f5f7fb;
  color: #1f2937;
}

.topbar {
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  padding: 18px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 10;
}

.brand {
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
}

nav {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.nav-btn,
.primary-btn,
.upload-form button {
  background: #e2e8f0;
  border: none;
  border-radius: 8px;
  padding: 10px 14px;
  cursor: pointer;
  font-weight: 600;
  color: #0f172a;
}

.nav-btn.active,
.primary-btn,
.upload-form button {
  background: #1d4ed8;
  color: #ffffff;
}

.container {
  max-width: 1300px;
  margin: 24px auto;
  padding: 0 18px 40px;
}

.panel {
  display: none;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
}

.panel.active {
  display: block;
}

h2 {
  margin-top: 0;
  color: #0f172a;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin: 18px 0;
}

.card {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 18px;
}

.card h3 {
  margin: 0 0 10px;
  font-size: 0.92rem;
  color: #475569;
}

.card .value {
  font-size: 1.7rem;
  font-weight: 700;
  color: #0f172a;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.chart-box {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 12px;
  min-height: 280px;
}

.chart-box.large {
  min-height: 320px;
}

.upload-form {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.status-box,
.summary-box,
.insights {
  margin-top: 18px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 16px;
}

.list {
  margin: 0;
  padding-left: 20px;
}

.table-container {
  margin-top: 20px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #e2e8f0;
  padding: 10px;
  text-align: left;
  font-size: 0.9rem;
}

th {
  background: #eef2ff;
}

@media (max-width: 768px) {
  .chart-grid {
    grid-template-columns: 1fr;
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
