# 💸 Smart Expense Tracker with ML Insights

A production-ready ML project for your portfolio — tracks daily expenses and uses machine learning to predict overspending and cluster your spending habits.

## 🚀 Live Demo Setup (2 minutes)

```bash
# 1. Clone / create project folder
mkdir smart-expense-tracker && cd smart-expense-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

App opens at → **http://localhost:8501**

---

## 🤖 Machine Learning Models Used

### 1. Linear Regression — Overspend Predictor
- **Input**: Monthly spending per category (Food, Transport, Shopping, etc.)
- **Output**: Predicted month-end total spend
- **Why it impresses**: Shows real-world regression usage with feature importance visualization

### 2. K-Means Clustering — Spending Habit Profiler
- **Input**: Normalized monthly category distributions
- **Output**: Spending personality — Balanced / Lifestyle / High Spender
- **Why it impresses**: Unsupervised learning on real user behavioral data

### 3. What-If Simulator
- Adjusts category spending via sliders
- Re-runs the model in real-time to show projected savings
- **Why it impresses**: Interactive ML inference — not just a static model

---

## 📁 Project Structure

```
smart-expense-tracker/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---


## 📊 Features

| Feature | Tech Used |
|---|---|
| Expense input form | Streamlit widgets |
| Category pie chart | Plotly |
| Monthly trend bar chart | Plotly |
| Overspend prediction | scikit-learn LinearRegression |
| Prediction gauge chart | Plotly Indicator |
| Feature importance chart | scikit-learn + Plotly |
| Spending habit clustering | scikit-learn KMeans |
| Category heatmap | Plotly density_heatmap |
| What-If simulator | Real-time ML inference |

---

*Built with Python · Streamlit · scikit-learn · Plotly*
