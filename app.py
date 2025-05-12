from src.simulate_traffic import generate_click_data
from src.detect_fraud import apply_simple_rules
import pandas as pd
import subprocess
import os
from src.generate_report import generate_summary_report


df = generate_click_data()
df.to_csv("data/click_logs.csv", index = False)

#df = pd.read_csv("data/click_logs.csv")
#df = apply_simple_rules(df)
#df.to_csv("data/click_logs_flagged.csv", index = False)
# Default rule values (baseline — not dynamic)

# Default rule values (baseline — not dynamic)
blacklisted_ips = ["192.168.0.1", "10.0.0.1"]
min_time_on_site = 2.0
ctr_threshold = 5
fraud_score_cutoff = 2

df = apply_simple_rules(
    df,
    blacklisted_ips=blacklisted_ips,
    min_time_on_site=min_time_on_site,
    ctr_threshold=ctr_threshold,
    fraud_score_cutoff=fraud_score_cutoff
)
generate_summary_report(df)


print("Clicks generated and saved to data/click_logs.csv")
see_viz = input("Would you like to view the Fraud Detection dashboard? (yes/no): ").strip().lower()

if see_viz in ["yes", "y"]:
    print("Launching dashboard...")
    subprocess.run(["streamlit", "run", "src/visualize_dashboard.py"])
else:
    print("Okay! Dashboard skipped. Report is saved to /reports/summary_report.md")
