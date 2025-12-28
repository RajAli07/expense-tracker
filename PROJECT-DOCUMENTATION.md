# Expense Tracker Pro
## Project Documentation

**Raj Ali**  
Full-Stack Developer  
ali.raj2511@gmail.com | New Delhi, India  
Flask | Python | Tailwind CSS | Chart.js  

---

## Table of Contents
1. Project Overview  
2. Key Features  
3. Technical Architecture  
4. User Interface  
5. Code Implementation  
6. Deployment Guide  
7. Live Demo & Repository  
8. Technical Challenges  
9. Future Roadmap  

---

## Project Overview

**Expense Tracker Pro** is a modern, responsive web application for personal finance management.  

**Objective:** Simplify expense tracking with real-time visualizations and export capabilities.  
**Duration:** 1 week (December 2025)  
**Status:** Production Ready | Live on Vercel  

*Replaces manual spreadsheets with intuitive dashboard, charts, and CSV export functionality.*

![Dashboard Overview](https://i.ibb.co/S7DJGrQb/Screenshot-2025-12-28-at-5-19-14-PM.png)

---

## Key Features

| Feature | Description |
|---------|-------------|
| Expense Entry | Category-based input (Food, Transport, Shopping) |
| Live Analytics | Real-time doughnut charts & summary statistics |
| Data Export | One-click CSV download |
| Responsive UI | Mobile + Desktop optimized |
| Dark Mode | Theme toggle functionality |
| Data Management | Add/Edit/Delete/Clear all operations |

![Features Showcase](https://uploads.onecompiler.io/43tk5a32h/448xcmcdw/Screenshot%202025-12-28%20at%2011.08.19%E2%80%AFPM.png)
 
 ## Data Export | One-click CSV download
![CSV Button](https://uploads.onecompiler.io/43tk5a32h/448xcmcdw/Screenshot%202025-12-29%20at%2012.09.02%E2%80%AFAM.png)
---

## Technical Architecture

Frontend: HTML5 | JavaScript | Tailwind CSS | Chart.js
Backend: Flask (Python) | Jinja2 Templates
Data Layer: JSON/CSV Storage
Deployment: Vercel | Render (Procfile ready)



**Core Components:**
app.py # Flask application & routes
templates/ # HTML + Jinja2
static/ # CSS/JS assets
requirements.txt # Dependencies



![Technical Architecture](https://uploads.onecompiler.io/43tk5a32h/448xcmcdw/generated-image.png)

---

## User Interface Screenshots

**Dashboard**  
Live charts | Recent transactions | Quick stats  
![Dashboard Overview](https://i.ibb.co/S7DJGrQb/Screenshot-2025-12-28-at-5-19-14-PM.png)

**Expenses Management**  
CRUD operations | Category filter | Search  
![Expenses Management](https://uploads.onecompiler.io/43tk5a32h/448xcmcdw/image%203.png)

**Analytics View**  
Spending breakdown | Total/Average metrics  
![Analytics View](https://uploads.onecompiler.io/43tk5a32h/448xcmcdw/image%202.png)

**Mobile Experience**  
Fully responsive design  
![Mobile Experience](https://uploads.onecompiler.io/43tk5a32h/448xcmcdw/Screenshot_2025-12-28-23-32-37-49_40deb401b9ffe8e1df2f1cc5ba480b12.jpg)


## Code Implementation

### 1. Flask Dashboard Route
@app.route('/')
def dashboard():
"""Render the main expense dashboard with summary and chart data."""
expenses = load_expenses()
summary = calculate_summary(expenses)
chart_data = prepare_chart_data(expenses)
return render_template('dashboard.html',
expenses=expenses,
summary=summary,
chart_data=chart_data)



### 2. CSV Export Endpoint
@app.route('/export_csv')
def export_csv():
"""Generate and download expenses data as CSV file."""
expenses = load_expenses()
csv_content = generate_csv(expenses)
return Response(
csv_content,
mimetype="text/csv",
headers={"Content-disposition": "attachment; filename=expenses.csv"}
)



### 3. Chart.js Integration
function renderChart(expenses) {
/* Render interactive doughnut chart for expense visualization */
const ctx = document.getElementById('expenseChart').getContext('2d');
new Chart(ctx, {
type: 'doughnut',
data: prepareChartData(expenses),
options: {
responsive: true,
maintainAspectRatio: false
}
});
}



![Development Environment](https://uploads.onecompiler.io/43tk5a32h/448xcmcdw/Screenshot%202025-12-28%20at%2011.37.43%E2%80%AFPM.png)

---

## Deployment & Setup

**Local Development:**
git clone https://github.com/RajAli07/expense-tracker

cd expense-tracker-pro
pip install -r requirements.txt
python app.py

Visit: http://localhost:5000


**Production Links:**
| Platform | Status | URL |
|----------|--------|-----|
| Vercel | Live | https://expensetrackerbyraj.vercel.app/|
| Render | Ready | Deploy via button |
| GitHub | Source | git@github.com:RajAli07/expense-tracker.git|

---

## Technical Challenges & Solutions

| Issue | Solution |
|-------|----------|
| f-string syntax | Fixed template escaping |
| Production deploy | Added Procfile + runtime.txt |
| Mobile charts | Chart.js responsive config |
| Data persistence | JSON/CSV hybrid storage |
| Theme switching | CSS custom properties |

---

## Future Enhancements
- User authentication system
- PostgreSQL database integration
- Monthly/yearly reporting
- Budget alerts & notifications
- Progressive Web App (PWA)

---

## Developer Information

**Rajali**  
Full-Stack Developer | Oracle Academy Student  

**Skills:** Python, Flask, SQL, JavaScript, Tailwind CSS  
**Learning:** Web Development | Database Systems | Deployment  

**Contact:**  
### Connect with me  

### Connect with me  

[![GitHub](https://img.shields.io/badge/GitHub-rajali07-black?logo=github&logoColor=white)](https://github.com/rajali07)  
[![Instagram](https://img.shields.io/badge/Instagram-@_asadstic_--E4405F?logo=instagram&logoColor=white)](https://www.instagram.com/_asadstic_/)  
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Chat-25D366?logo=whatsapp&logoColor=white)](https://wa.me/+916205440744)  
[![Email](https://img.shields.io/badge/Email-ali.raj2511@gmail.com-blue?logo=gmail&logoColor=white)](mailto:ali.raj2511@gmail.com)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-raj--ali07-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/raj-ali07)  
[![Portfolio](https://img.shields.io/badge/Portfolio-rajali07-663399?logo=vercel&logoColor=white)](https://rajaliportfolio.vercel.app/)  
[![YouTube](https://img.shields.io/badge/YouTube-Channel-FF0000?logo=youtube&logoColor=white)](#)  
[![Twitter](https://img.shields.io/badge/Twitter-Profile-1DA1F2?logo=twitter&logoColor=white)](https://x.com/its_raaz18413)

---

*© 2025 Raj Ali. All rights reserved. | Made in India ❤️*
