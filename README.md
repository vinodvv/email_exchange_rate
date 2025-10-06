# 💱 Exchange Rate Email Notifier

A simple Python application that fetches the **GBP to INR exchange rate** every day, saves it to a CSV file, and emails the latest rate to a specified recipient with a **styled HTML email**.

---

## 🚀 Features

- Fetches live GBP → INR rates using [ExchangeRate API](https://www.exchangerate-api.com/)
- Automatically saves daily rates to `exchange_rates.csv`
- Sends a professional HTML-formatted email with the latest rate
- Supports plain-text fallback for older email clients
- Environment variable–based credentials for security

---

## 🧰 Requirements

- Python 3.8 or later
- An ExchangeRate API key (free)
- Gmail account with an **App Password**

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vinodvv/email_exchange_rate.git
   cd email_exchange_rate

2. **Install dependencies
    ```bash
   pip install requests python-dotenv
3. **Create a .env file in the project root:
    ```bash
   API_KEY=your_exchangerateapi_key
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_gmail_app_password
   EMAIL_RECIPIENT=recipient@example.com
   SENDER_NAME=your name
   ⚠️ Important: Use an App Password, not your normal Gmail password.

## ▶️ Usage
Run the script manually:
   ```bash
python main.py
```
You will see output similar to:
   ```bash
Email sent successfully.
```
A record of exchange rates will be stored in exchange_rates.csv.

## 🧩 File Structure
```bash
email_exchange_rate/
│
├── main.py             # Main script
├── .env                # API and email credentials
├── exchange_rates.csv  # Saved daily rates
├── README.md           # Documentation
└── LICENSE             # MIT License
```

## 🕒 Optional: Automate Daily Email

You can schedule this script to run automatically every day.

## 📫 Email Preview

| 💱 Daily Exchange Rate Update     |
| --------------------------------- |
| **GBP → INR:** 106.42             |
| **Date:** 2025-10-04              |
| *Sent automatically by Vinod V V* |

## 🧑‍💻 Author

### Vinod V V

#### 📧 vinovijayan@gmail.com

#### 💼 https://www.linkedin.com/in/vinod-vv

## ⚖️ License

This project is licensed under the MIT License — see the LICENSE
 file for details.