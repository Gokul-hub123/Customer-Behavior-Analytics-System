# Customer Behavior Analytics System

A simple and professional Student Graduation Project (SGP) for analyzing customer behavior using Python, FastAPI, MySQL, Pandas, NumPy, Scikit-learn, and Chart.js.

## Project Objective
The project helps a retail business understand customer purchasing patterns, clean uploaded data, analyze sales, segment customers using RFM + K-Means, forecast sales, and generate a simple business report.

## Features
- Dashboard with KPI cards and charts
- Dataset upload through CSV file
- Data cleaning and validation
- Exploratory Data Analysis (EDA)
- Customer segmentation using RFM + K-Means
- Sales forecasting using Linear Regression
- Reports with insights
- Local Windows-friendly setup

## Tech Stack
- Frontend: HTML, CSS, JavaScript, Chart.js
- Backend: Python, FastAPI
- Data Processing: Pandas, NumPy
- Machine Learning: Scikit-learn
- Database: MySQL (with SQLite fallback for local testing)

## Folder Structure
```text
customer-behavior-analytics/
├── backend/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── routes/
│   │   ├── upload.py
│   │   ├── dashboard.py
│   │   ├── cleaning.py
│   │   ├── analysis.py
│   │   ├── segmentation.py
│   │   ├── forecasting.py
│   │   └── reports.py
│   └── services/
│       ├── data_processing.py
│       ├── analytics.py
│       ├── segmentation.py
│       ├── forecasting.py
│       └── reports.py
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/main.js
├── data/
│   └── sample_retail_data.csv
├── uploads/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── PROJECT_CONTEXT.md
└── sql/
    └── database.sql
```

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## MySQL Setup
1. Create a MySQL database named `customer_behavior_db`.
2. Configure `.env` using `.env.example`.
3. Example:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=customer_behavior_db
USE_MYSQL=false
```

## Run Backend
```bash
uvicorn backend.main:app --reload --port 8000
```

## Open Frontend
Open in browser:
```text
http://localhost:8000/
```

## Sample Dataset
A sample dataset is included in `data/sample_retail_data.csv` to test the system.

## How to Use
1. Open the dashboard.
2. Upload a CSV file.
3. Review dataset preview.
4. Clean data.
5. View EDA.
6. Run customer segmentation.
7. Generate forecast.
8. Open reports.

## Limitations
- This is designed as a simple and explainable SGP project.
- It uses a lightweight local architecture rather than a complex enterprise setup.
- Forecasting is simple linear regression for explainability.

## Future Scope
- Add MySQL-based storage for production
- Improve analytics with more data quality checks
- Add PDF report export
- Add login and user management

## Viva Explanation
This project helps businesses understand customer behavior, identify high-value customers, and forecast future sales using simple and explainable tools.
