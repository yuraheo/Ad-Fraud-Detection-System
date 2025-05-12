import pandas as pd
import random
from datetime import datetime, timedelta
import faker

fake = faker.Faker() # generate fake user data

def generate_click_data(n = 1000, fraud_ratio= 0.1):
    data = []
    for _ in range(n):
        is_fraud = random.random() < fraud_ratio
        ip = fake.ipv4_public() if not is_fraud else random.choice(['192.168.0.1', '10.0.0.1']) # Fraudsters always use one of two known bad IPs to simulate repeat spam sources while normal users get random IPs 
        timestamp = datetime.now() - timedelta(seconds = random.randint(0, 3600))
        user_id = fake.uuid4()
        session_id = fake.uuid4()
        device = random.choice(["mobile", "desktop", "tablet"])
        time_on_site = random.uniform(0.5, 300) if not is_fraud else random.uniform(0.1, 2)
        click_through = random.choice([True, False])

        data.append({
            'timestamp': timestamp,
            'ip': ip,
            'user_id': user_id,
            'session_id': session_id,
            'device': device,
            'time_on_site': round(time_on_site, 2),
            'click_through': click_through,
            'is_fraud': is_fraud
        })
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_click_data()
    df.to_csv("data/click_logs.csv", index=False)
    print("Generated 1000 fake ad click traffic")