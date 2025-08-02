# Statistical-Analysis-and-Data-mining-with-SQL
SQL project
# 📊 Statistical Analysis and Data Mining with SQL

## 📌 Objective

The aim of this project is to demonstrate how **PostgreSQL** can be used to perform statistical analysis and data mining on structured datasets. The system is designed to:
- Uncover hidden patterns
- Generate meaningful summaries
- Detect outliers
- Track and log analytical operations

---

## 🛠 Tools & Technologies

- **Database**: PostgreSQL (`26sqlll`)
- **Data Generation**: Python + Faker library
- **Client Interface**: pgAdmin4
- **Backend**: Flask (Python)
- **Frontend**: HTML + CSS

---

## 🧾 Database Tables

1. **Users**
   - `user_id` (INT, PK)
   - `name` (VARCHAR)
   - `role` (VARCHAR)

2. **Dataset**
   - `record_id` (INT, PK)
   - `category` (VARCHAR)
   - `value` (FLOAT)
   - `timestamp` (TIMESTAMP)
   - `label` (VARCHAR)

3. **Analysis Logs**
   - `log_id` (INT, PK)
   - `user_id` (INT, FK)
   - `operation` (TEXT)
   - `log_time` (TIMESTAMP)

---

## 🧪 SQL Functionalities

### ✅ Functions & Procedures

- **`compute_statistics()`**: Calculates average, median, and standard deviation.
- **`category_summaries()`**: Summarizes average value and total records per category.
- **`detect_outliers()`**: Identifies values more than 2 standard deviations from the mean.

### 📌 Views

- **`category_summary_view`**: Summary of each category with count, average, and sum.
- **`recent_operations_log`**: 10 most recent logs with user info.
- **`trendline_analysis`**: Daily average trends of values.

### 🔍 Nested Queries

- Top 5 highest values per category.
- Comparison of mean values across categories.
- Most frequent labels in each category.

### 🔗 Join-Based Queries

- Logs with user details.
- Daily activity logs of Analysts.
- Category and label distribution summary.

---

## 💡 Sample Queries

This project includes 20+ sample SQL queries for:
- Statistical summaries
- Trend analysis
- Label distributions
- Analyst activities
- Outlier detection

---

## 🧰 Data Generation

Used Python and the **Faker** library to generate 200 records for:
- Users
- Dataset
- Analysis Logs

All data is programmatically inserted using `psycopg2`.

---

## 🌐 Frontend Dashboard

The Flask-based web dashboard allows users to:
- View queries dynamically
- Get real-time outputs as HTML tables
- Explore data insights interactively

> Each query has a “View Query” and “View Output” button to toggle visibility.

---

## 📁 File Structure

