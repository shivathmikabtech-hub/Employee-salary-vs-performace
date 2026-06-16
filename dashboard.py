"""
Marketing & Sales Performance Dashboard — Friday Ready Version
Cleaner UI, plain-English insights, boss-friendly layout.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Marketing & Sales Performance",
    page_icon="📊",
    layout="wide",
)

# ============================================================
# CONFIGURATION
# ============================================================
TARGETS = {
    "caller": {"calls_per_day": 100, "leads_per_day": 20, "conversion_pct": 0.20,
               "weights": {"work": 0.4, "results": 0.4, "quality": 0.2}},
    "mailer": {"mails_per_day": 50, "leads_per_day": 50, "reply_rate": 0.10,
               "weights": {"work": 0.3, "results": 0.3, "quality": 0.4}},
    "sales":  {"demos_per_day": 4, "deals_per_week": 7, "close_rate": 0.33,
               "weights": {"work": 0.3, "results": 0.5, "quality": 0.2}},
}

EMPLOYEES = {
    "Lavanya": {"role": "Cold Caller", "type": "caller", "salary": 15000},
    "Mallika": {"role": "Cold Mailer", "type": "mailer", "salary": 22000},
    "Aruna":   {"role": "Cold Mailer", "type": "mailer", "salary": 22000},
    "Ganesh":  {"role": "Sales Demo",  "type": "sales",  "salary": 20000},
}

EXCEL_FILE = "Daily_Data_MarketingSales.xlsx"

# Custom CSS to reduce spacing
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
    }
    h1 {
        font-size: 1.8rem !important;
        padding-top: 0 !important;
        margin-top: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    h2, h3 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    [data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1F4E78;
    }
    hr {
        margin: 0.5rem 0 !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        margin-bottom: 0.3rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADER
# ============================================================
@st.cache_data
def load_data():
    try:
        caller_df = pd.read_excel(EXCEL_FILE, sheet_name="Caller_Data", header=2)
        mailer_df = pd.read_excel(EXCEL_FILE, sheet_name="Mailer_Data", header=2)
        sales_df  = pd.read_excel(EXCEL_FILE, sheet_name="Sales_Data",  header=2)
    except FileNotFoundError:
        st.error(f"Cannot find {EXCEL_FILE}. Place it in the same folder as dashboard.py")
        st.stop()

    def clean(df, cols):
        df = df.dropna(subset=["Employee Name"]).copy()
        df.columns = [c.strip() for c in df.columns]
        for col in cols:
            if col not in df.columns:
                df[col] = None
        df["Week #"] = pd.to_numeric(df["Week #"], errors="coerce")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df

    caller_df = clean(caller_df, ["Employee Name", "Week #", "Date", "Calls Made", "Leads Generated"])
    mailer_df = clean(mailer_df, ["Employee Name", "Week #", "Date", "Leads Researched", "Mails Sent", "Replies Received"])
    sales_df  = clean(sales_df,  ["Employee Name", "Week #", "Date", "Demos Given", "Deals Closed"])

    return caller_df, mailer_df, sales_df


# ============================================================
# SCORING ENGINE
# ============================================================
def score_caller(rows, target):
    days = len(rows)
    if days == 0:
        return None
    total_calls = rows["Calls Made"].sum()
    total_leads = rows["Leads Generated"].sum()
    conversion = total_leads / total_calls if total_calls else 0
    work_score    = min(100, total_calls / (target["calls_per_day"] * days) * 100)
    results_score = min(100, total_leads / (target["leads_per_day"] * days) * 100)
    quality_score = min(100, conversion / target["conversion_pct"] * 100)
    final = work_score * target["weights"]["work"] + results_score * target["weights"]["results"] + quality_score * target["weights"]["quality"]
    return {"Days Worked": days, "Total Work Done": total_calls, "Work Score": round(work_score, 1),
            "Total Results": total_leads, "Results Score": round(results_score, 1),
            "Success Rate %": round(conversion * 100, 1), "Quality Score": round(quality_score, 1),
            "Final Score": round(final, 1)}


def score_mailer(rows, target):
    days = len(rows)
    if days == 0:
        return None
    total_mails = rows["Mails Sent"].sum()
    total_leads = rows["Leads Researched"].sum()
    total_replies = rows["Replies Received"].sum()
    reply_rate = total_replies / total_mails if total_mails else 0
    work_score    = min(100, total_mails / (target["mails_per_day"] * days) * 100)
    results_score = min(100, total_leads / (target["leads_per_day"] * days) * 100)
    quality_score = min(100, reply_rate / target["reply_rate"] * 100)
    final = work_score * target["weights"]["work"] + results_score * target["weights"]["results"] + quality_score * target["weights"]["quality"]
    return {"Days Worked": days, "Total Work Done": total_mails, "Work Score": round(work_score, 1),
            "Total Results": total_leads, "Results Score": round(results_score, 1),
            "Success Rate %": round(reply_rate * 100, 1), "Quality Score": round(quality_score, 1),
            "Final Score": round(final, 1)}


def score_sales(rows, target, is_monthly=False):
    days = len(rows)
    if days == 0:
        return None
    total_demos = rows["Demos Given"].sum()
    total_deals = rows["Deals Closed"].sum()
    close_rate = total_deals / total_demos if total_demos else 0
    work_score = min(100, total_demos / (target["demos_per_day"] * days) * 100)
    target_deals = target["deals_per_week"] * (4 if is_monthly else 1)
    results_score = min(100, total_deals / target_deals * 100)
    quality_score = min(100, close_rate / target["close_rate"] * 100)
    final = work_score * target["weights"]["work"] + results_score * target["weights"]["results"] + quality_score * target["weights"]["quality"]
    return {"Days Worked": days, "Total Work Done": total_demos, "Work Score": round(work_score, 1),
            "Total Results": total_deals, "Results Score": round(results_score, 1),
            "Success Rate %": round(close_rate * 100, 1), "Quality Score": round(quality_score, 1),
            "Final Score": round(final, 1)}


def grade(score):
    if score >= 90: return "A — Excellent"
    if score >= 80: return "B — Good"
    if score >= 70: return "C — Average"
    if score >= 60: return "D — Below Avg"
    return "E — Poor"


def compute_scores(caller_df, mailer_df, sales_df, week=None, month=None):
    results = []
    for name, info in EMPLOYEES.items():
        emp_type = info["type"]
        if emp_type == "caller":
            df = caller_df[caller_df["Employee Name"] == name]
        elif emp_type == "mailer":
            df = mailer_df[mailer_df["Employee Name"] == name]
        else:
            df = sales_df[sales_df["Employee Name"] == name]

        if week is not None:
            df = df[df["Week #"] == week]
        elif month is not None:
            df = df[(df["Week #"] >= month*4-3) & (df["Week #"] <= month*4)]

        target = TARGETS[emp_type]
        is_monthly = month is not None

        if emp_type == "caller":
            s = score_caller(df, target)
        elif emp_type == "mailer":
            s = score_mailer(df, target)
        else:
            s = score_sales(df, target, is_monthly=is_monthly)

        if s is None:
            continue

        s["Employee"] = name
        s["Role"] = info["role"]
        s["Monthly Salary"] = info["salary"]
        s["Grade"] = grade(s["Final Score"])
        results.append(s)

    return pd.DataFrame(results)


def add_ranking_and_value(df, is_monthly=False):
    if df.empty:
        return df
    df = df.sort_values(["Final Score", "Employee"], ascending=[False, True]).reset_index(drop=True)
    df["Rank"] = df.index + 1
    if is_monthly:
        df["Cost per Day Worked"] = (df["Monthly Salary"] / df["Days Worked"]).round(0)
    else:
        df["Cost per Day Worked"] = ((df["Monthly Salary"] / 4) / df["Days Worked"]).round(0)
    df["Daily Salary Cost"] = (df["Monthly Salary"] / 22).round(0)
    df["Cost per Score Point"] = (df["Cost per Day Worked"] / df["Final Score"]).round(2)
    df["Value Rank"] = df["Cost per Score Point"].rank(method="min").astype(int)
    return df


def insight_text(row):
    """Generate plain-English insight for each employee."""
    name = row["Employee"]
    score = row["Final Score"]
    role = row["Role"]

    if score >= 90:
        verdict = "is performing excellently"
    elif score >= 80:
        verdict = "is doing well"
    elif score >= 70:
        verdict = "is performing average"
    elif score >= 60:
        verdict = "is underperforming"
    else:
        verdict = "needs immediate attention"

    # Role-specific detail
    if row["Work Score"] >= 90 and row["Quality Score"] < 70:
        detail = "— putting in volume but quality is low"
    elif row["Quality Score"] >= 90 and row["Work Score"] < 70:
        detail = "— high quality work but volume is low"
    elif row["Work Score"] < 60:
        detail = "— activity volume is below target"
    elif row["Results Score"] < 60:
        detail = "— outputs are below target"
    else:
        detail = ""

    return f"**{name}** ({role}) {verdict} {detail}"


# ============================================================
# LOAD DATA
# ============================================================
caller_df, mailer_df, sales_df = load_data()

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("📊 Filters")
view_mode = st.sidebar.radio("View Mode", ["Weekly", "Monthly"])

all_weeks = sorted(set(caller_df["Week #"].dropna().unique()) |
                   set(mailer_df["Week #"].dropna().unique()) |
                   set(sales_df["Week #"].dropna().unique()))
all_weeks = [int(w) for w in all_weeks if pd.notna(w)]

if not all_weeks:
    st.warning("No data found. Please add data to the Excel file.")
    st.stop()

if view_mode == "Weekly":
    selected = st.sidebar.selectbox("Select Week", all_weeks, index=len(all_weeks)-1)
    scores_df = compute_scores(caller_df, mailer_df, sales_df, week=selected)
    period_label = f"Week {selected}"
else:
    max_month = max(1, (max(all_weeks) + 3) // 4)
    selected = st.sidebar.selectbox("Select Month", list(range(1, max_month + 1)), index=0)
    scores_df = compute_scores(caller_df, mailer_df, sales_df, month=selected)
    period_label = f"Month {selected} (Weeks {selected*4-3}–{selected*4})"

scores_df = add_ranking_and_value(scores_df, is_monthly=(view_mode == "Monthly"))

st.sidebar.markdown("---")
st.sidebar.markdown("### 🖨️ Save Report")
st.sidebar.markdown("Press **Ctrl+P** in browser to print or save as PDF for boss.")

# ============================================================
# MAIN — HEADER
# ============================================================
st.markdown(f"## 📊 Marketing & Sales Performance — {period_label}")

# ============================================================
# KPI BANNER — Top Highlights
# ============================================================
if not scores_df.empty:
    top = scores_df.iloc[0]
    bottom = scores_df.iloc[-1]
    avg_score = scores_df["Final Score"].mean()
    best_value = scores_df.sort_values("Value Rank").iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏆 Top Performer", top["Employee"], f"Score: {top['Final Score']:.1f}")
    c2.metric("📊 Team Average", f"{avg_score:.1f}", "out of 100")
    c3.metric("💰 Best Value", best_value["Employee"], f"₹{best_value['Cost per Score Point']:.0f}/pt")
    c4.metric("⚠️ Needs Attention", bottom["Employee"], f"Score: {bottom['Final Score']:.1f}")

st.markdown("---")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Ranking", "📋 Performance Details", "💰 Salary vs Performance", "📈 Visual Insights", "📖 How Scores Are Calculated"])
# --- TAB 1: RANKING ---
with tab1:
    st.subheader(f"Team Ranking — {period_label}")

    # Style the ranking dataframe with color
    rank_view = scores_df[["Rank", "Employee", "Role", "Final Score", "Grade"]].copy()

    def color_score(val):
        if val >= 90:
            return "background-color: #d4edda; color: black"
        elif val >= 80:
            return "background-color: #e2f0d9; color: black"
        elif val >= 70:
            return "background-color: #fff3cd; color: black"
        elif val >= 60:
            return "background-color: #fce4d6; color: black"
        else:
            return "background-color: #f8d7da; color: black"

    styled = rank_view.style.map(color_score, subset=["Final Score"])
    st.dataframe(styled, use_container_width=True, hide_index=True, height=180)
    st.markdown("---")
    st.markdown("#### 💡 What This Means")
    for _, row in scores_df.iterrows():
        st.markdown(f"- {insight_text(row)}")

# --- TAB 2: PERFORMANCE DETAILS ---
with tab2:
    st.subheader(f"Performance Breakdown — {period_label}")
    st.caption("Simple view: what each employee did and how they scored.")

    detail = scores_df[["Employee", "Role", "Days Worked", "Total Work Done",
                        "Total Results", "Final Score", "Grade"]].copy()

    def color_final(val):
        if val >= 90:
            return "background-color: #d4edda; font-weight: bold"
        elif val >= 80:
            return "background-color: #e2f0d9; font-weight: bold"
        elif val >= 70:
            return "background-color: #fff3cd; font-weight: bold"
        elif val >= 60:
            return "background-color: #fce4d6; font-weight: bold"
        else:
            return "background-color: #f8d7da; font-weight: bold"

    styled = detail.style.map(color_final, subset=["Final Score"]).format({
        "Final Score": "{:.1f}",
        "Total Work Done": "{:.0f}",
        "Total Results": "{:.0f}",
        "Days Worked": "{:.0f}",
    })
    st.dataframe(styled, use_container_width=True, hide_index=True, height=180)

    st.markdown("#### 📖 What Each Column Means")
    st.markdown("""
    - **Total Work Done**: Calls made (Lavanya) / Mails sent (Mallika, Aruna) / Demos given (Ganesh)
    - **Total Results**: Leads generated / Leads researched / Deals closed
    - **Final Score**: Overall performance (out of 100)
    - **Grade**: A=Excellent, B=Good, C=Average, D=Below Average, E=Poor
    """)

# --- TAB 3: SALARY VS PERFORMANCE ---
with tab3:
    st.subheader(f"Salary vs Performance — {period_label}")
    st.caption("Are you getting your money's worth from each employee?")

    sal_view = scores_df[["Employee", "Role", "Monthly Salary", "Final Score",
                          "Daily Salary Cost", "Cost per Day Worked",
                          "Cost per Score Point", "Value Rank"]].copy()

    def color_val_rank(val):
        if val == 1:
            return "background-color: #d4edda; color: black"
        elif val == scores_df["Value Rank"].max():
            return "background-color: #f8d7da; color: black"
        return ""

    # styled = sal_view.style.map(color_val_rank, subset=["Value Rank"])
    # st.dataframe(styled, use_container_width=True, hide_index=True, height=180)
    styled = sal_view.style.map(color_val_rank, subset=["Value Rank"]).format({
        "Monthly Salary": "₹{:,.0f}",
        "Final Score": "{:.1f}",
        "Daily Salary Cost": "₹{:,.0f}",
        "Cost per Day Worked": "₹{:,.0f}",
        "Cost per Score Point": "₹{:.2f}",
        "Value Rank": "{:.0f}",
    })
    st.dataframe(styled, use_container_width=True, hide_index=True, height=180)
    st.markdown("#### 📖 How to Read This")
    st.markdown("""
    - **Daily Salary Cost** = What you pay this employee per day (Monthly Salary ÷ 22 days)
    - **Cost per Day Worked** = Real cost when they actually show up
    - **Cost per Score Point** = Money spent per point of performance — **lower is better**
    - **Value Rank 1** = Best value for money (green), highest rank = worst value (red)
    """)

    # Quick verdicts
    st.markdown("#### 💡 Salary Insights")
    best_val = scores_df.sort_values("Value Rank").iloc[0]
    worst_val = scores_df.sort_values("Value Rank", ascending=False).iloc[0]
    st.success(f"💎 **Best Value:** {best_val['Employee']} delivers ₹{best_val['Cost per Score Point']:.0f} per score point — most cost-effective employee.")
    st.error(f"⚠️ **Lowest Value:** {worst_val['Employee']} costs ₹{worst_val['Cost per Score Point']:.0f} per score point — most expensive per output.")
                                                                                                                                                          
# --- TAB 4: VISUAL INSIGHTS ---
with tab4:
    st.subheader(f"Visual Insights — {period_label}")

    if not scores_df.empty:
        # Bar chart: Who's performing best
        fig_bar = px.bar(
            scores_df.sort_values("Final Score"),
            x="Final Score", y="Employee", orientation="h",
            color="Final Score",
            color_continuous_scale=[(0, "#b95052"), (0.5, "#dcc23f"), (1, "#3A9C54")],
            title="🏆 Who's Performing Best?",
            text="Final Score",
            range_color=[0, 100],
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_bar.update_layout(height=400, showlegend=False, xaxis_range=[0, 110])
        st.plotly_chart(fig_bar, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            # Score breakdown
            comp_df = scores_df.melt(
                id_vars=["Employee"],
                value_vars=["Work Score", "Results Score", "Quality Score"],
                var_name="Component", value_name="Score"
            )
            fig_comp = px.bar(
                comp_df, x="Employee", y="Score", color="Component", barmode="group",
                title="🔍 What's Driving Each Score?",
                color_discrete_map={"Work Score": "#5B9BD5", "Results Score": "#ED7D31", "Quality Score": "#70AD47"}
            )
            fig_comp.update_layout(height=400)
            st.plotly_chart(fig_comp, use_container_width=True)

        with col2:
            # Salary vs Score scatter
            fig_scatter = px.scatter(
                scores_df, x="Monthly Salary", y="Final Score",
                size="Days Worked", color="Final Score",
                text="Employee",
                title="💰 Salary vs Performance",
                color_continuous_scale=[(0, "#f8696b"), (0.5, "#ffeb84"), (1, "#63be7b")],
                size_max=50,
                range_color=[0, 100],
            )
            fig_scatter.update_traces(textposition="top center")
            fig_scatter.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Weekly trend
        if view_mode == "Weekly" and len(all_weeks) > 1:
            st.markdown("### 📈 Performance Trend Across Weeks")
            trend_rows = []
            for wk in all_weeks:
                wk_scores = compute_scores(caller_df, mailer_df, sales_df, week=wk)
                for _, row in wk_scores.iterrows():
                    trend_rows.append({"Week": f"Week {wk}", "Employee": row["Employee"], "Final Score": row["Final Score"]})

            if trend_rows:
                trend_df = pd.DataFrame(trend_rows)
                fig_line = px.line(
                    trend_df, x="Week", y="Final Score", color="Employee",
                    markers=True, title="Who's Improving? Who's Declining?",
                )
                fig_line.update_layout(height=400, yaxis_range=[0, 110])
                st.plotly_chart(fig_line, use_container_width=True)

# --- TAB 5: HOW SCORES ARE CALCULATED ---
with tab5:
    st.subheader("📖 How Performance Scores Are Calculated")
    st.caption("Reference guide — explains every formula in plain English.")

    st.markdown("### 🎯 The Scoring System")
    st.markdown("""
    Every employee gets a **Final Score out of 100**, made up of 3 sub-scores:

    - **Work Score** → How much activity they did (volume)
    - **Results Score** → What they achieved (outputs)
    - **Quality Score** → How good their work was (success rate)

    Each sub-score uses this universal formula:
    """)
    st.info("**Sub-Score = MIN(100, (Actual ÷ Target) × 100)**\n\nCapped at 100 — exceeding target doesn't give extra credit.")

    st.markdown("---")

    # ---- CALLER ----
    st.markdown("### 🎯 Lavanya — Cold Caller")
    caller_table = pd.DataFrame({
        "Metric": ["Work Score", "Results Score", "Quality Score", "Final Score"],
        "Formula": [
            "(Total Calls ÷ (100 × Days)) × 100",
            "(Total Leads ÷ (20 × Days)) × 100",
            "(Conversion% ÷ 20%) × 100",
            "Work × 40% + Results × 40% + Quality × 20%",
        ],
        "Target": ["100 calls/day", "20 leads/day", "20% conversion", "—"],
        "Example": [
            "485 calls ÷ (100×5) × 100 = 97",
            "90 leads ÷ (20×5) × 100 = 90",
            "(90÷485)/0.20 × 100 = 93",
            "97×0.4 + 90×0.4 + 93×0.2 = 93.4",
        ],
    })
    st.dataframe(caller_table, use_container_width=True, hide_index=True)
    st.caption("**Why these weights?** Calls + Leads equally important (40% each). Conversion already reflects in leads, so 20%.")

    st.markdown("---")

    # ---- MAILER ----
    st.markdown("### 📧 Mallika & Aruna — Cold Mailers")
    mailer_table = pd.DataFrame({
        "Metric": ["Work Score", "Results Score", "Quality Score", "Final Score"],
        "Formula": [
            "(Mails Sent ÷ (50 × Days)) × 100",
            "(Leads Researched ÷ (50 × Days)) × 100",
            "(Reply Rate ÷ 10%) × 100",
            "Work × 30% + Results × 30% + Quality × 40%",
        ],
        "Target": ["50 mails/day", "50 leads/day", "10% reply rate", "—"],
        "Example": [
            "255 mails ÷ (50×5) × 100 = 102 → capped at 100",
            "260 leads ÷ (50×5) × 100 = 104 → capped at 100",
            "(25÷255)/0.10 × 100 ≈ 98",
            "100×0.3 + 100×0.3 + 98×0.4 = 99.2",
        ],
    })
    st.dataframe(mailer_table, use_container_width=True, hide_index=True)
    st.caption("**Why these weights?** Reply rate matters MOST (40%) — sending 1000 spam emails with no replies is worthless.")

    st.markdown("---")

    # ---- SALES ----
    st.markdown("### 💼 Ganesh — Sales Demo Person")
    sales_table = pd.DataFrame({
        "Metric": ["Work Score", "Results Score", "Quality Score", "Final Score"],
        "Formula": [
            "(Demos Given ÷ (4 × Days)) × 100",
            "(Deals Closed ÷ 7) × 100",
            "(Close Rate ÷ 33%) × 100",
            "Work × 30% + Results × 50% + Quality × 20%",
        ],
        "Target": ["4 demos/day", "7 deals/week", "33% close rate", "—"],
        "Example": [
            "18 demos ÷ (4×5) × 100 = 103 → 100",
            "7 deals ÷ 5 × 100 = 140 → 100",
            "(7÷18)/0.33 × 100 = 118 → 100",
            "100×0.3 + 100×0.5 + 100×0.2 = 100",
        ],
    })
    st.dataframe(sales_table, use_container_width=True, hide_index=True)
    st.caption("**Why these weights?** Deals closed = revenue. Results weighted 50% because closed deals are what make money.")

    st.markdown("---")

    # ---- GRADES ----
    st.markdown("### 🏅 Performance Grades")
    grade_table = pd.DataFrame({
        "Score Range": ["90 – 100", "89 – 80", "79 – 70", "69 – 60", "Below 50"],
        "Grade": ["A — Excellent", "B — Good", "C — Average", "D — Below Average", "E — Poor"],
    })
    st.dataframe(grade_table, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ---- SALARY METRICS ----
    st.markdown("### 💰 Salary vs Performance Metrics")
    salary_table = pd.DataFrame({
        "Metric": ["Daily Salary Cost", "Cost per Day Worked", "Cost per Score Point", "Value Rank"],
        "Formula": [
            "Monthly Salary ÷ 22",
            "(Monthly Salary ÷ 4) ÷ Days Worked",
            "Cost per Day Worked ÷ Final Score",
            "Rank by Cost per Score Point (1 = best value)",
        ],
        "What It Means": [
            "What you pay per working day",
            "Real cost when they actually show up",
            "Money spent per point of performance — LOWER IS BETTER",
            "Best value-for-money employee",
        ],
        "Example (Lavanya)": [
            "₹15,000 ÷ 22 = ₹682/day",
            "(₹15,000 ÷ 4) ÷ 5 days = ₹750/day",
            "₹750 ÷ 93.4 = ₹8/point",
            "Rank 1 → cheapest per point of output",
        ],
    })
    st.dataframe(salary_table, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ---- TARGETS REFERENCE ----
    st.markdown("### 🎯 Targets Reference")
    targets_table = pd.DataFrame({
        "Role": ["Cold Caller (Lavanya)", "Cold Mailer (Mallika, Aruna)", "Sales Demo (Ganesh)"],
        "Daily Activity Target": ["100 calls + 20 leads", "50 mails + 50 leads researched", "4 demos/day"],
        "Weekly Output Target": ["500 calls + 100 leads", "250 mails + 250 leads", "7 deals/week"],
        "Quality Benchmark": ["20% conversion", "10% reply rate", "33% close rate"],
    })
    st.dataframe(targets_table, use_container_width=True, hide_index=True)
    st.caption("Industry-standard benchmarks for B2B cold outreach. Adjust if CEO sets different targets.")

    st.markdown("---")

    # # ---- KEY QUESTIONS ----
    # st.markdown("### ❓ Common Questions (Cheat Sheet)")
    # with st.expander("**Why is Lavanya not 100?**"):
    #     st.write("She made 485 calls (target 500) and got 90 leads (target 100), so she's slightly below 100% on activity and results. Her conversion is around 18.5% — close to the 20% benchmark.")
    # with st.expander("**Why are Mallika and Ganesh both 100?**"):
    #     st.write("T hey hit or exceeded all 3 targets — activity, results, and quality. The system caps at 100 so super-performers all look the same. Look at raw numbers to differentiate.")
    # with st.expander("**Why does Ganesh weight deals at 50%?**"):
    #     st.write("Sales people are measured on revenue. Demos are activity but deals are what make money. So deals carry double the weight of demos in his final score.")
    # with st.expander("**How is Cost per Score Point useful?**"):
    #     st.write("It shows ROI per rupee paid. Lavanya at ₹8/point means we get a lot of performance per rupee. Aruna at ₹14/point is more expensive for the same output level — even though her salary is higher.")
    # with st.expander("**Why is Aruna scoring lower than Mallika?**"):
    #     st.write("Same role, same salary, but different output. Aruna sent fewer mails (185 vs 255), generated fewer leads (200 vs 260). It's an effort/skill gap — worth a 1-on-1 conversation.")

st.markdown("---")