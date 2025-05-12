# Ad Fraud Summary Report
**Generated on:** 2025-05-12 09:56:06

**Total Clicks:** 1000
**Click-Through Rate (CTR):** 51.5%
**Fraudulent Clicks Detected:** 113
**Legitimate Clicks:** 887

## Top Suspicious IPs
- 192.168.0.1: 68 flagged clicks
- 10.0.0.1: 41 flagged clicks
- 151.210.126.4: 1 flagged clicks
- 158.141.22.110: 1 flagged clicks
- 200.79.166.87: 1 flagged clicks

## Detection Rules Used:
- Known bad IPs
- Short time on site (< {df['time_on_site'].min()}s)
- Low CTR proxy (click_through field)
- Score threshold as set in the dashboard
