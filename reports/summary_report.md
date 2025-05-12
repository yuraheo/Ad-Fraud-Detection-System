# Ad Fraud Summary Report
**Generated on:** 2025-05-12 09:46:56

**Total Clicks:** 1000
**Click-Through Rate (CTR):** 49.3%
**Fraudulent Clicks Detected:** 94
**Legitimate Clicks:** 906

## Top Suspicious IPs
- 10.0.0.1: 51 flagged clicks
- 192.168.0.1: 41 flagged clicks
- 175.48.47.230: 1 flagged clicks
- 189.70.214.170: 1 flagged clicks

## Detection Rules Used:
- Known bad IPs
- Short time on site (< {df['time_on_site'].min()}s)
- Low CTR proxy (click_through field)
- Score threshold as set in the dashboard
