import pandas as pd
from datetime import datetime

def generate_summary_report(df, output_file="reports/summary_report.md"):

    total_clicks = len(df)
    total_fraud = df['flagged_as_fraud'].sum()
    total_legit = total_clicks - total_fraud
    ctr = round((df['click_through'].sum() / total_clicks) * 100, 2)

    fraud_by_ip = df[df['flagged_as_fraud']].groupby('ip').size().sort_values(ascending=False).head(5)

    with open(output_file, "w") as f:
        f.write(f"# Ad Fraud Summary Report\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Clicks:** {total_clicks}\n")
        f.write(f"**Click-Through Rate (CTR):** {ctr}%\n")
        f.write(f"**Fraudulent Clicks Detected:** {total_fraud}\n")
        f.write(f"**Legitimate Clicks:** {total_legit}\n\n")
        
        f.write(f"## Top Suspicious IPs\n")
        for ip, count in fraud_by_ip.items():
            f.write(f"- {ip}: {count} flagged clicks\n")

        f.write(f"\n## Detection Rules Used:\n")
        f.write("- Known bad IPs\n")
        f.write("- Short time on site (< {df['time_on_site'].min()}s)\n")
        f.write("- Low CTR proxy (click_through field)\n")
        f.write("- Score threshold as set in the dashboard\n")

    print(f"Summary report saved to: {output_file}")

if __name__ == "__main__":
    generate_summary_report()