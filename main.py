import csv
import os
import requests
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime


def load_credentials():
    """
    Load API key, email credentials from a .env file
    """
    load_dotenv()
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    api_key = os.getenv("API_KEY")
    return email_address, email_password, api_key


def get_exchange_rate(api_key):
    """
    Fetch the current GBP to INR exchange rate from ExchangeRate API
    """
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/GBP"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["result"] != "success":
            raise ValueError("API returned error response")

        rate = data["conversion_rates"].get("INR")
        if rate is None:
            raise ValueError("INR rate missing from API data")

        date_utc_str = data["time_last_update_utc"]
        date_obj = datetime.strptime(date_utc_str, "%a, %d %b %Y %H:%M:%S %z")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        return formatted_date, rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None, None


def save_exchange_rate(date, rate, filepath="exchange_rates.csv"):
    """
    Append the latest exchange rate to a CSV file
    """
    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["date", "GBP_INR_Rate"])
        writer.writerow([date, rate])


def load_exchange_rates(filepath="exchange_rates.csv"):
    """
    Load all stored exchange rates from the CSV file.
    """
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def login_to_email(email_address, email_password):
    """
    Log in to the Gmail SMTP server
    """
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(email_address, email_password)
    return smtp


def create_email(rate, sender_name, recipient):
    """
    Create an email with both plain text and HTML content
    """
    msg = EmailMessage()
    msg['Subject'] = f"💱 Today's GBP to INR Exchange Rate"
    msg['From'] = sender_name
    msg['To'] = recipient

    # Plain text fallback
    text_content = (
        f"Hi Jayasree,\n\n"
        f"Today's exchange rate:\n"
        f"GBP → INR: {rate['GBP_INR_Rate']}\n"
        f"Date: {rate['date']}\n\n"
        f"Regards,\nVinod V V"
    )

    # HTML version (simple + elegant)
    html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color:#f9f9f9; margin:0; padding:0;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td align="center" style="padding: 20px;">
                        <table style="max-width: 600px; background-color:#ffffff; border-radius:10px; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                            <tr>
                                <td align="center" style="font-size: 24px; color: #0078d7; font-weight: bold;">
                                    💱 Daily Exchange Rate Update
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 20px 0; font-size: 16px; color: #333;">
                                    <p>Hi Jayasree,</p>
                                    <p>Here's today's exchange rate:</p>
                                    <table width="100%" cellpadding="10" style="border-collapse: collapse;">
                                        <tr style="background-color: #0078d7; color: white;">
                                            <th align="left">Base Currency</th>
                                            <th align="left">Target Currency</th>
                                            <th align="left">Rate</th>
                                        </tr>
                                        <tr style="background-color: #f2f2f2;">
                                            <td>GBP</td>
                                            <td>INR</td>
                                            <td><strong>{rate['GBP_INR_Rate']}</strong></td>
                                        </tr>
                                    </table>
                                    <p style="margin-top: 20px; color:#555;">Date: {rate['date']}</p>
                                    <p style="margin-top: 20px;">Regards,<br><b>Vinod V V</b></p>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="font-size: 12px; color: #999; padding-top: 10px;">
                                    © {datetime.now().year} Exchange Rate Notifier | Auto-generated email
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype="html")
    # msg.set_content(f"Exchange Rate (GBP-INR): {rate['GBP_INR_Rate']}\n"
    #                 f"Date: {rate['date']}\n")
    return msg


def main():
    """
    Main function that fetches exchange rate, stores it, and emails the user.
    """
    email_address, email_password, api_key = load_credentials()
    recipient = os.getenv("EMAIL_RECIPIENT")
    sender_name = os.getenv("SENDER_NAME", email_address)

    date, rate = get_exchange_rate(api_key)
    if not date or not rate:
        print("Exchange rate fetch failed. Exiting.")
        return

    save_exchange_rate(date, rate)

    exchange_rates = load_exchange_rates()
    today = datetime.now().strftime("%Y-%m-%d")

    smtp = login_to_email(email_address, email_password)

    for rate in exchange_rates:
        if rate['date'] == today:
            msg = create_email(rate, sender_name, recipient)
            smtp.send_message(msg)
            print("Email sent successfully.")
            break
    smtp.quit()


if __name__ == "__main__":
    main()
