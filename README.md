# 📊 Marketing & Sales Performance Dashboard

A comprehensive **Streamlit-based Business Intelligence Dashboard** built to monitor, evaluate, and visualize the performance of Marketing and Sales teams. This application transforms raw Excel data into meaningful insights by automating KPI calculations, employee performance scoring, rankings, salary efficiency analysis, and interactive visualizations.

The dashboard is designed for **business owners, startup founders, managers, HR teams, and sales leaders** who need a simple yet powerful solution to measure employee productivity and make data-driven decisions.

---

# 🚀 Project Overview

Managing employee performance manually using Excel sheets can become time-consuming and error-prone. This dashboard eliminates manual calculations by automatically reading employee activity data from Excel and generating professional reports with actionable insights.

The application supports multiple roles such as:

* 📞 Cold Callers
* 📧 Cold Mailers
* 💼 Sales Executives

Each role is evaluated using customized performance metrics and weighted scoring models to ensure fair assessment based on job responsibilities.

---

# ✨ Key Features

## 📊 Interactive Dashboard

* Clean and modern Streamlit interface
* Business-friendly layout
* KPI Cards for quick performance overview
* Responsive design

---

## 📅 Weekly & Monthly Reports

Switch between

* Weekly Performance
* Monthly Performance

to analyze employee growth over different time periods.

---

## 🏆 Automated Employee Ranking

Employees are automatically ranked based on their overall performance score.

Includes

* Rank
* Grade (A–E)
* Final Performance Score
* Role
* Employee Details

---

## 🎯 Intelligent Performance Scoring

Every employee receives a score out of **100** based on three major performance categories.

### Work Score

Measures activity volume such as

* Calls Made
* Emails Sent
* Demos Conducted

---

### Results Score

Measures actual business outcomes

* Leads Generated
* Leads Researched
* Deals Closed

---

### Quality Score

Measures efficiency

* Conversion Rate
* Reply Rate
* Deal Closing Rate

---

Each employee's final score is calculated using customizable weighted formulas depending on their role.

Example:

```
Final Score =
Work Score × Weight +
Results Score × Weight +
Quality Score × Weight
```

---

## 💰 Salary vs Performance Analysis

One of the major highlights of this dashboard.

Automatically calculates

* Monthly Salary
* Daily Salary Cost
* Cost per Day Worked
* Cost per Performance Point
* Value Ranking

This helps management identify

* Highest ROI employees
* Underperforming employees
* Salary efficiency

---

## 📈 Interactive Visualizations

Built using Plotly Express.

Includes

* Performance Bar Charts
* Salary vs Performance Scatter Charts
* Score Component Comparison
* Weekly Trend Analysis
* Team Performance Comparison

All charts are interactive.

---

## 📖 Built-in Formula Reference

A dedicated section explains

* Every KPI
* Every Formula
* Performance Weightage
* Score Calculation Logic

This makes the dashboard easy to understand for managers without technical knowledge.

---

## 💡 Smart Employee Insights

Automatically generates easy-to-understand performance summaries such as

> "Ganesh is performing excellently."

> "Lavanya has high activity but quality needs improvement."

> "Mallika delivers the best value for money."

These insights are generated dynamically based on employee performance.

---

# 📂 Project Structure

```
Marketing-Sales-Dashboard
│
├── dashboard.py
├── Daily_Data_MarketingSales.xlsx
├── requirements.txt
├── README.md
└── screenshots/
```

---

# 📁 Data Source

The dashboard reads data directly from an Excel workbook.

Supported sheets include

* Caller_Data
* Mailer_Data
* Sales_Data

The application automatically

* Cleans missing values
* Converts dates
* Validates columns
* Calculates KPIs
* Generates reports

No manual calculations are required.

---

# 📊 KPIs Included

* Total Calls Made
* Total Emails Sent
* Leads Generated
* Leads Researched
* Replies Received
* Demos Given
* Deals Closed
* Conversion Rate
* Reply Rate
* Closing Rate
* Work Score
* Results Score
* Quality Score
* Final Performance Score
* Employee Grade
* Team Average
* Top Performer
* Best Value Employee
* Employee Ranking

---

# 📑 Dashboard Sections

## 🏆 Ranking

Displays

* Employee Rank
* Performance Score
* Grades
* Role

---

## 📋 Performance Details

Shows

* Days Worked
* Total Work Done
* Results Achieved
* Final Score
* Grade

---

## 💰 Salary vs Performance

Provides

* Salary Analysis
* Cost per Score
* Value Ranking
* ROI Insights

---

## 📈 Visual Insights

Interactive charts including

* Employee Performance
* Salary vs Score
* Weekly Trends
* Component Breakdown

---

## 📖 Scoring Guide

Complete explanation of

* Performance formulas
* KPI calculations
* Weight distribution
* Target benchmarks

---

# 🎯 Performance Evaluation Logic

### Cold Caller

Metrics

* Calls Made
* Leads Generated
* Conversion Rate

Weight Distribution

* Work → 40%
* Results → 40%
* Quality → 20%

---

### Cold Mailer

Metrics

* Emails Sent
* Leads Researched
* Reply Rate

Weight Distribution

* Work → 30%
* Results → 30%
* Quality → 40%

---

### Sales Executive

Metrics

* Demos Given
* Deals Closed
* Closing Rate

Weight Distribution

* Work → 30%
* Results → 50%
* Quality → 20%

---

# 🛠 Technologies Used

* Python
* Streamlit
* Pandas
* Plotly Express
* OpenPyXL
* Excel
* CSS (Streamlit Styling)

---

# 📦 Python Libraries

```
streamlit
pandas
plotly
openpyxl
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

Clone the repository

```bash
git clone https://github.com/yourusername/Marketing-Sales-Dashboard.git
```

Navigate to the project folder

```bash
cd Marketing-Sales-Dashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run dashboard.py
```

---

# 🎯 Business Benefits

* Eliminates manual reporting
* Automates KPI calculation
* Measures employee productivity
* Tracks performance trends
* Improves management decisions
* Identifies high-performing employees
* Highlights employees requiring improvement
* Calculates employee ROI
* Saves reporting time
* Provides management-ready dashboards

---

# 👨‍💻 Future Enhancements

* Database Integration (MySQL/PostgreSQL)
* User Authentication
* Admin Panel
* Power BI Integration
* PDF Report Export
* Email Report Automation
* Real-time Data Synchronization
* Predictive Performance Analytics
* Attendance Integration
* Lead Management Module

---

# ⭐ If you found this project useful

Consider giving the repository a **⭐ Star** and feel free to contribute by submitting issues, feature requests, or pull requests. Your feedback and contributions are always welcome!
