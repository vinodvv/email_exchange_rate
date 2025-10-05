import csv
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


with open("exchange_rates.csv") as file:
    reader = csv.DictReader(file)
    exchange_rates = list(reader)


for rate in exchange_rates:
    msg = EmailMessage()
    msg['Subject'] = "Today's GBP INR Exchange Rate"
    msg['From'] = "Vinod VV"
    msg['To'] = "vinovijayan@hotmail.com"
    msg.set_content(f"Exchange Rate (GBP-INR): {rate['GBP_INR_Rate']}\n"
                    f"Date: {rate['date']}\n ")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
