import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import hashlib
import json
import warnings
warnings.filterwarnings("ignore")

# ─── File Storage ────────────────────────────────────────────────────────────
DATA_FILE = "expenses.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
        if not df.empty:
            return df
    return generate_sample_data(3)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# ─── User Auth ───────────────────────────────────────────────────────────────
USERS_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        return json.load(open(USERS_FILE))
    return {}

def save_users(users):
    json.dump(users, open(USERS_FILE, "w"))

def show_login():
    st.markdown("""
    <div style='max-width:380px; margin:80px auto; text-align:center;'>
        <div style='font-size:48px;'>💸</div>
        <h2 style='font-family:DM Sans,sans-serif; font-weight:700; margin-bottom:4px;'>Smart Expense Tracker</h2>
        <p style='color:#888; margin-bottom:32px;'>ML-powered spending insights</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

        with tab_login:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login_btn = st.form_submit_button("Login", use_container_width=True)
                if login_btn:
                    users = load_users()
                    if username in users and users[username]["password"] == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.data_file = f"expenses_{username}.csv"
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")

        with tab_signup:
            with st.form("signup_form"):
                new_user = st.text_input("Choose Username")
                new_pass = st.text_input("Choose Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                signup_btn = st.form_submit_button("Create Account", use_container_width=True)
                if signup_btn:
                    if not new_user or not new_pass:
                        st.error("Please fill all fields")
                    elif new_pass != confirm_pass:
                        st.error("❌ Passwords do not match")
                    else:
                        users = load_users()
                        if new_user in users:
                            st.error("❌ Username already exists")
                        else:
                            users[new_user] = {"password": hash_password(new_pass)}
                            save_users(users)
                            st.success("✅ Account created! Please login.")


# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.metric-card {
    background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    color: white;
}
.metric-label { font-size: 12px; color: #a0a0c0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.metric-value { font-size: 28px; font-weight: 700; color: #e2e2ff; }
.metric-sub { font-size: 12px; color: #7c7c9a; margin-top: 4px; }

.insight-box {
    background: rgba(139,92,246,0.08);
    border-left: 3px solid #8b5cf6;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    font-size: 14px;
    color: #c4c4e0;
}
.cluster-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
}
.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #4f46e5);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 1.5rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    transition: all 0.2s;
}
.stButton > button:hover { opacity: 0.85; transform: translateY(-1px); }
</style>
""", unsafe_allow_html=True)


# ─── Sample Data Generator ──────────────────────────────────────────────────
CATEGORIES = ["Food & Dining", "Transport", "Shopping", "Entertainment", "Health", "Utilities", "Education", "Others"]
CAT_COLORS = {
    "Food & Dining": "#f97316", "Transport": "#3b82f6", "Shopping": "#ec4899",
    "Entertainment": "#a855f7", "Health": "#22c55e", "Utilities": "#eab308",
    "Education": "#06b6d4", "Others": "#94a3b8"
}

def generate_sample_data(months=3):
    rows = []
    base = datetime.today().replace(day=1)
    for m in range(months):
        month_start = (base - timedelta(days=30*m)).replace(day=1)
        n = random.randint(25, 40)
        for _ in range(n):
            cat = random.choices(CATEGORIES, weights=[25,15,20,10,8,10,7,5])[0]
            budgets = {"Food & Dining":8000,"Transport":3000,"Shopping":6000,
                       "Entertainment":2500,"Health":2000,"Utilities":2500,
                       "Education":1500,"Others":1000}
            amount = round(np.random.normal(budgets[cat]/10, budgets[cat]/20), 2)
            amount = max(50, amount)
            day = random.randint(1, 28)
            rows.append({
                "Date": month_start.replace(day=day),
                "Category": cat,
                "Amount": amount,
                "Description": f"{cat} expense"
            })
    return pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)


# ─── ML: Monthly Overspend Predictor ────────────────────────────────────────
def train_overspend_model(df, budget):
    df["Month"] = df["Date"].dt.to_period("M")
    monthly = df.groupby(["Month","Category"])["Amount"].sum().unstack(fill_value=0).reset_index()
    monthly["Total"] = monthly[CATEGORIES].sum(axis=1)
    monthly["DayOfMonth"] = 28
    monthly["Overspent"] = (monthly["Total"] > budget).astype(int)

    if len(monthly) < 2:
        return None, None

    X = monthly[CATEGORIES].values
    y = monthly["Total"].values
    model = LinearRegression().fit(X, y)
    return model, monthly


def predict_this_month(df, model, budget):
    current_month = datetime.today().replace(day=1).strftime("%Y-%m")
    this_month = df[df["Date"].dt.strftime("%Y-%m") == current_month]
    if this_month.empty:
        return None, None, None
    spent_by_cat = this_month.groupby("Category")["Amount"].sum()
    X_now = np.array([[spent_by_cat.get(c, 0) for c in CATEGORIES]])
    predicted = model.predict(X_now)[0]
    days_elapsed = datetime.today().day
    daily_rate = this_month["Amount"].sum() / days_elapsed
    projected = daily_rate * 30
    return predicted, projected, this_month["Amount"].sum()


# ─── ML: Spending Habit Clustering ──────────────────────────────────────────
def cluster_spending(df):
    monthly = df.groupby([df["Date"].dt.to_period("M"), "Category"])["Amount"].sum().unstack(fill_value=0)
    if len(monthly) < 2:
        return None, None

    scaler = StandardScaler()
    X = scaler.fit_transform(monthly.values)
    k = min(3, len(monthly))
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    monthly["Cluster"] = labels

    cluster_names = {
        0: ("🧘 Balanced Spender", "#22c55e"),
        1: ("🛍️ Lifestyle Spender", "#ec4899"),
        2: ("⚡ High Spender", "#f97316"),
    }
    return monthly, cluster_names


# ─── AUTH GATE ──────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login()
    st.stop()

# Per-user data file
DATA_FILE = st.session_state.get("data_file", "expenses_default.csv")

# ─── SESSION STATE ──────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df
df["Date"] = pd.to_datetime(df["Date"])


# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## 💸 Smart Expense Tracker")
    st.caption(f"👤 Logged in as **{st.session_state.get('username', '')}**")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    st.markdown("---")

    st.markdown("### ➕ Add Expense")
    with st.form("add_expense"):
        date = st.date_input("Date", datetime.today())
        category = st.selectbox("Category", CATEGORIES)
        amount = st.number_input("Amount (₹)", min_value=1.0, value=500.0, step=10.0)
        desc = st.text_input("Description", placeholder="e.g. Lunch, Uber, Netflix...")
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            new_row = pd.DataFrame([{"Date": pd.to_datetime(date), "Category": category,
                                      "Amount": amount, "Description": desc}])
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            save_data(st.session_state.df)
            st.success("✅ Expense saved!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎯 Monthly Budget")
    budget = st.number_input("Set Budget (₹)", min_value=1000, value=25000, step=500)

    st.markdown("---")
    if st.button("🔄 Reset to Sample Data"):
        st.session_state.df = generate_sample_data(3)
        save_data(st.session_state.df)
        st.rerun()


# ─── HEADER ─────────────────────────────────────────────────────────────────
st.markdown("# 💸 Smart Expense Tracker")
st.markdown("*ML-powered spending insights & predictions*")
st.markdown("---")

# ─── TOP METRICS ────────────────────────────────────────────────────────────
current_month = datetime.today().strftime("%Y-%m")
this_month_df = df[df["Date"].dt.strftime("%Y-%m") == current_month]
total_this_month = this_month_df["Amount"].sum()
total_all = df["Amount"].sum()
days_elapsed = datetime.today().day
daily_avg = total_this_month / max(days_elapsed, 1)
projected_eom = daily_avg * 30
budget_used_pct = (total_this_month / budget) * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Spent This Month", f"₹{total_this_month:,.0f}", f"Budget: ₹{budget:,}")
with col2:
    delta = f"{'⚠️ Over' if projected_eom > budget else '✅ Under'} budget"
    st.metric("📈 Projected Month-End", f"₹{projected_eom:,.0f}", delta)
with col3:
    st.metric("📅 Daily Average", f"₹{daily_avg:,.0f}", f"{days_elapsed} days elapsed")
with col4:
    pct_color = "normal" if budget_used_pct < 80 else "inverse"
    st.metric("🎯 Budget Used", f"{budget_used_pct:.1f}%", f"₹{max(0, budget - total_this_month):,.0f} remaining")


# ─── TABS ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🤖 ML Predictions", "🧬 Spending Habits", "🔮 What-If Simulator"])


# ── TAB 1: Overview ──────────────────────────────────────────────────────────
with tab1:
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("### Spending by Category")
        cat_totals = df.groupby("Category")["Amount"].sum().reset_index()
        fig_pie = px.pie(cat_totals, names="Category", values="Amount",
                         color="Category", color_discrete_map=CAT_COLORS,
                         hole=0.45)
        fig_pie.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=320,
                               legend=dict(font_size=12))
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.markdown("### Monthly Spending Trend")
        monthly_total = df.groupby(df["Date"].dt.strftime("%b %Y"))["Amount"].sum().reset_index()
        monthly_total.columns = ["Month", "Total"]
        fig_bar = px.bar(monthly_total, x="Month", y="Total",
                         color_discrete_sequence=["#7c3aed"],
                         text_auto=".2s")
        fig_bar.add_hline(y=budget, line_dash="dash", line_color="#ef4444",
                          annotation_text=f"Budget ₹{budget:,}")
        fig_bar.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=320,
                               yaxis_title="Amount (₹)", xaxis_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### Daily Spending Heatmap (This Month)")
    if not this_month_df.empty:
        daily = this_month_df.groupby(this_month_df["Date"].dt.day)["Amount"].sum().reset_index()
        daily.columns = ["Day", "Amount"]
        fig_line = px.area(daily, x="Day", y="Amount",
                           color_discrete_sequence=["#8b5cf6"],
                           labels={"Amount": "₹ Spent", "Day": "Day of Month"})
        fig_line.update_layout(height=200, margin=dict(t=10,b=0,l=0,r=0))
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("### Recent Transactions")
    display_df = df.sort_values("Date", ascending=False).head(20).copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
    display_df["Amount"] = display_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(display_df[["Date","Category","Description","Amount"]],
                 use_container_width=True, hide_index=True)


# ── TAB 2: ML Predictions ─────────────────────────────────────────────────
with tab2:
    st.markdown("### 🤖 Overspend Prediction — Linear Regression")
    st.caption("Model trained on your past monthly spending patterns per category")

    model, monthly_data = train_overspend_model(df, budget)

    if model is None:
        st.info("Add more data (at least 2 months) to enable predictions.")
    else:
        predicted, projected, spent_so_far = predict_this_month(df, model, budget)

        col1, col2 = st.columns(2)
        with col1:
            if predicted:
                diff = predicted - budget
                st.markdown(f"""
                **ML Model Prediction for This Month:**
                - Spent so far: ₹{spent_so_far:,.0f}
                - Model predicts month-end total: **₹{predicted:,.2f}**
                - Budget gap: {'🔴 ₹' + f'{abs(diff):,.0f} OVER budget' if diff > 0 else '🟢 ₹' + f'{abs(diff):,.0f} under budget'}
                """)

                gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=predicted,
                    delta={"reference": budget, "valueformat": ",.0f",
                           "prefix": "₹", "relative": False},
                    title={"text": "Predicted vs Budget (₹)"},
                    gauge={
                        "axis": {"range": [0, budget * 1.5], "tickformat": ",.0f"},
                        "bar": {"color": "#7c3aed"},
                        "steps": [
                            {"range": [0, budget * 0.7], "color": "#dcfce7"},
                            {"range": [budget * 0.7, budget], "color": "#fef9c3"},
                            {"range": [budget, budget * 1.5], "color": "#fee2e2"},
                        ],
                        "threshold": {"line": {"color": "#dc2626", "width": 3},
                                      "thickness": 0.75, "value": budget}
                    }
                ))
                gauge.update_layout(height=300, margin=dict(t=30,b=0,l=20,r=20))
                st.plotly_chart(gauge, use_container_width=True)

        with col2:
            st.markdown("**Feature Importance — Which categories drive your spending?**")
            importance = pd.DataFrame({
                "Category": CATEGORIES,
                "Coefficient": model.coef_
            }).sort_values("Coefficient", ascending=True)
            fig_imp = px.bar(importance, x="Coefficient", y="Category",
                             orientation="h", color="Coefficient",
                             color_continuous_scale=["#ddd6fe","#7c3aed","#4f46e5"])
            fig_imp.update_layout(height=300, margin=dict(t=0,b=0,l=0,r=0),
                                   coloraxis_showscale=False)
            st.plotly_chart(fig_imp, use_container_width=True)

        st.markdown("---")
        st.markdown("### 📅 Historical Predictions vs Actuals")
        if monthly_data is not None:
            monthly_data["Predicted"] = model.predict(monthly_data[CATEGORIES].values)
            monthly_data["Month_str"] = monthly_data["Month"].astype(str)
            fig_vs = go.Figure()
            fig_vs.add_trace(go.Bar(name="Actual", x=monthly_data["Month_str"],
                                    y=monthly_data["Total"], marker_color="#7c3aed"))
            fig_vs.add_trace(go.Scatter(name="Predicted", x=monthly_data["Month_str"],
                                        y=monthly_data["Predicted"],
                                        line=dict(color="#f97316", width=2, dash="dot"),
                                        mode="lines+markers"))
            fig_vs.add_hline(y=budget, line_dash="dash", line_color="#ef4444",
                             annotation_text="Budget")
            fig_vs.update_layout(height=300, margin=dict(t=10,b=0,l=0,r=0),
                                  yaxis_title="Amount (₹)")
            st.plotly_chart(fig_vs, use_container_width=True)


# ── TAB 3: Spending Habits (Clustering) ──────────────────────────────────
with tab3:
    st.markdown("### 🧬 Spending Habit Analysis — K-Means Clustering")
    st.caption("Identifies your spending personality based on category distribution patterns")

    monthly_clusters, cluster_names = cluster_spending(df)

    if monthly_clusters is None:
        st.info("Need at least 2 months of data for habit clustering.")
    else:
        latest_cluster = monthly_clusters["Cluster"].iloc[-1]
        name, color = cluster_names.get(latest_cluster, ("Unknown", "#gray"))

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style='background:{color}22; border:2px solid {color}; border-radius:12px; padding:1.2rem; text-align:center;'>
                <div style='font-size:32px;'>{name.split()[0]}</div>
                <div style='font-size:16px; font-weight:600; color:{color}; margin-top:8px;'>{' '.join(name.split()[1:])}</div>
                <div style='font-size:12px; color:#888; margin-top:8px;'>Your latest spending profile</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**What this means:**")
            profiles = {
                0: "You maintain a healthy balance across all categories. Your spending is consistent and predictable — a great sign!",
                1: "You tend to spend heavily on lifestyle categories like shopping and entertainment. Consider setting sub-limits.",
                2: "Your total spending is high across multiple categories. The ML model flags this month as a high-spend period.",
            }
            st.info(profiles.get(latest_cluster, "Unique spending pattern detected."))

        with col2:
            st.markdown("**Monthly Category Breakdown**")
            cat_cols = [c for c in CATEGORIES if c in monthly_clusters.columns]
            monthly_clusters["Month_str"] = monthly_clusters.index.astype(str)
            fig_stack = px.bar(monthly_clusters.reset_index(), x="Month_str", y=cat_cols,
                               color_discrete_map=CAT_COLORS, barmode="stack")
            fig_stack.update_layout(height=320, margin=dict(t=0,b=0,l=0,r=0),
                                     xaxis_title="", yaxis_title="Amount (₹)",
                                     legend=dict(font_size=11))
            st.plotly_chart(fig_stack, use_container_width=True)

        st.markdown("### Top Spending Categories Analysis")
        cat_monthly = df.groupby(["Category", df["Date"].dt.strftime("%b %Y")])["Amount"].sum().reset_index()
        fig_hm = px.density_heatmap(cat_monthly, x="Date", y="Category", z="Amount",
                                     color_continuous_scale="Purples",
                                     labels={"Date": "Month", "Amount": "₹"})
        fig_hm.update_layout(height=300, margin=dict(t=10,b=0,l=0,r=0))
        st.plotly_chart(fig_hm, use_container_width=True)


# ── TAB 4: What-If Simulator ──────────────────────────────────────────────
with tab4:
    st.markdown("### 🔮 What-If Savings Simulator")
    st.caption("Adjust spending by category and see ML-predicted impact on your month-end total")

    model2, _ = train_overspend_model(df, budget)

    if model2 is None:
        st.info("Need more data to run simulations.")
    else:
        st.markdown("**Drag sliders to simulate spending cuts (%)**")
        current_cats = this_month_df.groupby("Category")["Amount"].sum() if not this_month_df.empty else pd.Series({c: 1000 for c in CATEGORIES})

        reductions = {}
        cols = st.columns(2)
        for i, cat in enumerate(CATEGORIES):
            with cols[i % 2]:
                reductions[cat] = st.slider(f"{cat}", 0, 100, 0, 5,
                                             format="%d%% cut",
                                             key=f"slider_{cat}")

        simulated = {}
        for cat in CATEGORIES:
            base = current_cats.get(cat, 0)
            simulated[cat] = base * (1 - reductions[cat] / 100)

        X_sim = np.array([[simulated.get(c, 0) for c in CATEGORIES]])
        sim_predicted = model2.predict(X_sim)[0]
        original_predicted = model2.predict(np.array([[current_cats.get(c, 0) for c in CATEGORIES]]))[0]
        savings = original_predicted - sim_predicted

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Original Prediction", f"₹{original_predicted:,.0f}")
        with col2:
            st.metric("✨ Simulated Prediction", f"₹{sim_predicted:,.0f}",
                      delta=f"-₹{savings:,.0f}" if savings > 0 else "No change")
        with col3:
            st.metric("💚 Projected Savings", f"₹{max(0, savings):,.0f}",
                      delta="vs original plan")

        # Comparison chart
        comparison_df = pd.DataFrame({
            "Category": CATEGORIES,
            "Current": [current_cats.get(c, 0) for c in CATEGORIES],
            "Simulated": [simulated[c] for c in CATEGORIES]
        })
        fig_comp = px.bar(comparison_df.melt(id_vars="Category", var_name="Scenario", value_name="Amount"),
                          x="Category", y="Amount", color="Scenario", barmode="group",
                          color_discrete_map={"Current": "#7c3aed", "Simulated": "#22c55e"})
        fig_comp.update_layout(height=320, margin=dict(t=10,b=0,l=0,r=0),
                                xaxis_title="", yaxis_title="Amount (₹)",
                                xaxis_tickangle=-30)
        st.plotly_chart(fig_comp, use_container_width=True)


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#666; font-size:12px;'>"
    "Built with Streamlit · scikit-learn · Plotly &nbsp;|&nbsp; "
    "ML Models: Linear Regression + K-Means Clustering"
    "</div>",
    unsafe_allow_html=True
)
