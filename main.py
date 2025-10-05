import csv
import os
import requests
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
api_key = os.getenv("API_KEY")

url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/GBP"

response = requests.get(url)
data = response.json()

rate = data["conversion_rates"].get("INR")

date_utc_str = data["time_last_update_utc"]

date_obj = datetime.strptime(date_utc_str, "%a, %d %b %Y %H:%M:%S %z")

formatted_date = date_obj.strftime("%Y-%m-%d")

with open("exchange_rates.csv", "a") as file:
    writer = csv.writer(file)
    writer.writerow([formatted_date, rate])

with open("exchange_rates.csv") as file:
    reader = csv.DictReader(file)
    exchange_rates = list(reader)

today = datetime.now().strftime("%Y-%m-%d")

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(email_address, email_password)

    for rate in exchange_rates:
        if rate['date'] == today:
            msg = EmailMessage()
            msg['Subject'] = "Today's GBP INR Exchange Rate"
            msg['From'] = "Vinod VV"
            msg['To'] = "vinovijayan@hotmail.com"
            msg.set_content(f"Exchange Rate (GBP-INR): {rate['GBP_INR_Rate']}\n"
                            f"Date: {rate['date']}\n ")
            smtp.send_message(msg)
