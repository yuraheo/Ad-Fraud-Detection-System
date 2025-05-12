import pandas as pd

# Apply fraud detection rules to df
def apply_simple_rules(df, blacklisted_ips, min_time_on_site, ctr_threshold, fraud_score_cutoff):
    df['fraud_score'] = 0 

    # Rule 1: known bad IP addresses +1
    df.loc[df['ip'].isin([ip.strip() for ip in blacklisted_ips]), 'fraud_score'] += 1


    # Rule 2: extreamly short time on site (under 2 seconds) +1
    df.loc[df['time_on_site'] < min_time_on_site, 'fraud_score'] += 1

    # Rule 3: No click through AND short session +1 
    df['click_binary'] = df['click_through'].astype(int)
    df.loc[df['click_binary'] * 100 < ctr_threshold, 'fraud_score'] += 1
    
    # Flag as fraud if score >= 2
    df['flagged_as_fraud'] = df['fraud_score'] >= fraud_score_cutoff

    return df

# If this file is run directly (not imported), apply the rules and save output
if __name__ == "__main__":
    df = pd.read_csv("data/click_logs.csv")  # Load the click data from CSV
    df = apply_simple_rules(df)             # Apply the fraud detection rules
    df.to_csv("data/click_logs_flagged.csv", index=False)  # Save results with flags
    print(f"Fraud detection complete. Flagged {df['flagged_as_fraud'].sum()} records.")

