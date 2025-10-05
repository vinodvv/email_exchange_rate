import csv
import smtplib
from email.message import EmailMessage


with open("exchange_rates.csv") as file:
    reader = csv.DictReader(file)
    exchange_rates = list(reader)


for rate in exchange_rates:
    msg = EmailMessage()
    msg['Subject'] = "Today's GBP INR Exchange Rate"
    msg['From'] = "vinovijayan@gmail.com"
    msg['To'] = "vinovijayan@gmail.com"
    msg.set_content(f"Exchange Rate (GBP-INR): {rate['GBP_INR_Rate']}\n"
                    f"Date: {rate['date']}\n ")
    print(msg)
