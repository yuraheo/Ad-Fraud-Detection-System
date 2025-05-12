import streamlit as st
from detect_fraud import apply_simple_rules
import pandas as pd
import matplotlib.pyplot as plt
from generate_report import generate_summary_report


# visualize fraud dection insights
# calculate CTR
st.set_page_config(page_title = "Ad Fraud Dashboard", layout = "centered")

df = pd.read_csv("data/click_logs.csv")

st.sidebar.title("Fraud Rule Editor")

# Editable fraud rule controls
blacklisted_ips = st.sidebar.text_area(
    "Blacklisted IPs (comma-separated)",
    value="192.168.0.1,10.0.0.1"
).split(",")

min_time_on_site = st.sidebar.slider(
    "Minimum Time on Site (seconds)",
    min_value=0.0, max_value=10.0, value=2.0, step=0.1
)

ctr_threshold = st.sidebar.slider(
    "CTR Threshold (%)",
    min_value=0, max_value=100, value=5
)

fraud_score_cutoff = st.sidebar.slider(
    "Fraud Score Cutoff",
    min_value=1, max_value=5, value=2
)

df = apply_simple_rules(
    df,
    blacklisted_ips=blacklisted_ips,
    min_time_on_site=min_time_on_site,
    ctr_threshold=ctr_threshold,
    fraud_score_cutoff=fraud_score_cutoff
)
if st.sidebar.button("Generate Summary Report"):
    output_path = "reports/summary_report.md"
    generate_summary_report(df)
    st.sidebar.success("Report generated at: reports/summary_report.md")
    with open(output_path, "r") as f:
        report_text = f.read()

    st.subheader("Summary Report")
    st.code(report_text, language='markdown')

    # Download button
    with open(output_path, "rb") as f:
        st.download_button(
            label="Download Report (Markdown)",
            data=f,
            file_name="ad_fraud_summary_report.md",
            mime="text/markdown"
        )


total_clicks = len(df)
total_click_throughs = df['click_through'].sum()
ctr = round((total_click_throughs / total_clicks) * 100, 2)
total_flagged = df['flagged_as_fraud'].sum()

st.title("Ad Fraud Detection Dashboard")

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Clicks", total_clicks)
col2.metric("Click_Through Rate (CTR)", f"{ctr}%")
col3.metric("Flagged as Fraud", f"{total_flagged}")

st.divider()

st.subheader("Top Suspicous IPs")
top_ips = df[df['flagged_as_fraud']].groupby("ip").size().sort_values(ascending = False).head(10)
st.bar_chart(top_ips)

st.subheader("Time on Site Distribution")
fig1, ax1 = plt.subplots()
df['time_on_site'].plot.hist(bins = 30, ax = ax1 )
ax1.set_xlabel("Time on Site (seconds)")
ax1.set_ylabel("Number of Clicks")
st.pyplot(fig1)


st.subheader("Fraud Score Histogram")
fig2 , ax2 = plt.subplots()
df['fraud_score'].plot.hist(bins = range(0, df['fraud_score'].max()+2), rwidth = 0.8, ax = ax2)
ax2.set_xlabel("Fraud Score")
ax2.set_ylabel("Number of Clicks")
st.pyplot(fig2)
st.subheader("What Do Fraud Scores Mean?")
st.markdown(f"""
Each click is given a **fraud score** based on suspicious behavior:

- **0** - Normal click, no red flags.
- **1** - One suspicious signal (e.g., short time on site or known bad IP).
- **2** - Medium suspicion. Likely bot or click farm.
- **3 or more** -🚨 Highly suspicious behavior. Strong fraud indicators.

> Any click with a score **≥ {fraud_score_cutoff}** is flagged as fraud in this system.
""")


st.divider()

with st.expander("See Raw Data"):
    st.dataframe(df)