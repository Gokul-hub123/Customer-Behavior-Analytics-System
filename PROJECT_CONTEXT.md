# Customer Behavior Analytics System

## 1. Project Title
Customer Behavior Analytics System

## 2. Introduction
This project is a simple and professional Student Graduation Project (SGP) designed to analyze customer buying patterns, segment customers, forecast future sales, and generate a report from a retail dataset. The project uses Python, FastAPI, Pandas, NumPy, Scikit-learn, MySQL, and Chart.js.

## 3. Problem Statement
Retail businesses often collect large amounts of sales data but struggle to understand customer behavior, product demand, and future sales trends. This project provides a simple local solution to upload data, clean it, analyze trends, segment customers, forecast sales, and produce business-oriented insights.

## 4. Objectives
- Upload a retail CSV dataset.
- Clean and validate the dataset.
- Analyze sales and customer purchasing behavior.
- Use RFM + K-Means clustering.
- Forecast future monthly sales using linear regression.
- Generate a simple business report.

## 5. Proposed Solution
The project uses a FastAPI backend to handle uploads and analytics, while the frontend is built using HTML, CSS, and JavaScript. Dashboard metrics, charts, and results are generated from the uploaded dataset and stored in CSV and database tables for future access.

## 6. Features
- Dashboard with KPI cards and charts
- Dataset upload and preview
- Data cleaning summary and cleaning process
- EDA using real data
- Customer segmentation using RFM + K-Means
- Sales forecasting using Linear Regression
- Reports with findings
- CSV plus MySQL-compatible storage

## 7. Technology Stack
- Frontend: HTML, CSS, JavaScript, Chart.js
- Backend: Python, FastAPI
- Data processing: Pandas, NumPy
- Database: MySQL + SQLite fallback
- Machine learning: Scikit-learn

## 8. System Architecture
The frontend communicates with the FastAPI backend using REST API endpoints. The backend handles dataset upload, cleaning, analysis, clustering, and forecasting.

## 9. Database Design
- customers: customer_id, customer_name
- products: product_id, product_name, category
- transactions: transaction_id, customer_id, product_id, transaction_date, quantity, unit_price, total_amount
- customer_segments: customer_id, recency, frequency, monetary, cluster, cluster_label
- forecasts: forecast_month, predicted_sales, model_name, mae, rmse

## 10. Data Processing
The system validates, normalizes column names, converts date and numeric fields, removes invalid rows, and generates clean transaction data before analysis.

## 11. EDA
The EDA module calculates sales totals, averages, category contribution, product contribution, and monthly sales behavior using actual dataset values.

## 12. Customer Segmentation
Customer segmentation uses RFM (Recency, Frequency, Monetary) and K-Means Clustering to group customers into segments based on purchasing behavior.

## 13. Sales Forecasting
The system calculates monthly sales and trains a Linear Regression model to forecast the next three months. Forecasts are displayed with notes that they are estimates only.

## 14. Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 15. MySQL Setup
1. Create a MySQL database named `customer_behavior_db`.
2. Update `.env` using `.env.example`.
3. Example:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=customer_behavior_db
USE_MYSQL=false
```

If MySQL is unavailable, the project automatically runs in SQLite fallback mode.

## 16. How to Run
```bash
uvicorn backend.main:app --reload --port 8000
```

Open the browser at:
```text
http://localhost:8000/
```

## 17. How to Use
1. Open the Dashboard.
2. Upload a CSV file.
3. Review the dataset preview.
4. Clean the data.
5. View EDA results.
6. Run customer segmentation.
7. Generate forecast.
8. Open the report page.

## 18. Limitations
- This is a simple project for academic purposes.
- Forecasting uses a basic linear trend model.
- MySQL is optional for local use and can be replaced with SQLite fallback.

## 19. Future Scope
- Add PDF report export.
- Improve validation for more retail datasets.
- Add dashboard filters and export options.
- Add more detailed customer behavior analysis.

## 20. Viva Explanation
This project helps a business understand customer purchase behavior, identify high-value customers, estimate future sales, and generate actionable insights using simple and explainable analytics methods.
