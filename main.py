import csv
import os
import requests
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime


def load_credentials():
    load_dotenv()
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    api_key = os.getenv("API_KEY")
    return email_address, email_password, api_key


def get_exchange_rate(api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/GBP"
    response = requests.get(url)
    data = response.json()
    rate = data["conversion_rates"].get("INR")
    date_utc_str = data["time_last_update_utc"]
    date_obj = datetime.strptime(date_utc_str, "%a, %d %b %Y %H:%M:%S %z")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date, rate


def save_exchange_rate(date, rate):
    with open("exchange_rates.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([date, rate])


def load_exchange_rates(filepath="exchange_rates.csv"):
    with open(filepath) as file:
        reader = csv.DictReader(file)
        exchange_rates = list(reader)
        return exchange_rates


def login_to_email(email_address, email_password):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(email_address, email_password)
    return smtp


def create_email(rate):
    msg = EmailMessage()
    msg['Subject'] = "Today's GBP INR Exchange Rate"
    msg['From'] = "Vinod VV"
    msg['To'] = "vinovijayan@hotmail.com"
    msg.set_content(f"Exchange Rate (GBP-INR): {rate['GBP_INR_Rate']}\n"
                    f"Date: {rate['date']}\n ")
    return msg


email_address, email_password, api_key = load_credentials()
date, rate = get_exchange_rate(api_key)
save_exchange_rate(date, rate)

exchange_rates = load_exchange_rates()
smtp = login_to_email(email_address, email_password)

today = datetime.now().strftime("%Y-%m-%d")

for rate in exchange_rates:
    if rate['date'] == today:
        msg = create_email(rate)
        smtp.send_message(msg)
