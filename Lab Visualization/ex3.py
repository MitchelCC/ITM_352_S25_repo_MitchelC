import matplotlib.pyplot as plt
import json
import requests

file_id = "1-kvj2Ore88PGzZ9J7_lPBOvNf5C1ohpQ"
url = f"https://drive.google.com/uc?export=download&id={file_id}"

response = requests.get(url)
response.raise_for_status

data = json.loads(response.text)
filtered_data = [
    trip for trip in data
    if 'payment_type' in trip and trip ["payment_type"].strip()
    and "tips" in trip and trip ["tips"].strip()
]
from collections import defaultdict
tips_by_payment = defaultdict(float)

tips_by_payment = defaultdict(float)
for trip in filtered_data: 
    payment = trip["payment_type"].strip()
    tips = float (trip["tips"])
    tips_by_payment[payment] += tips


payment_types = list (tips_by_payment.keys())
total_tips = list (tips_by_payment.values())

plt.bar(payment_types, total_tips, color = 'skyblue', edgecolor ='black')
plt.xlabel("Payment Method")
plt.ylabel("Total Tips ($)")
plt.title("Total Tips by Payment Method (Trips from Area 8)")
plt.xticks(rotation=45, ha='right')  # Rotate labels for readability
plt.tight_layout()
plt.show()