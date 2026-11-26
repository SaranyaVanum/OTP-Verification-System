
# 🔐 OTP Verification System

A Python-based email OTP verification application with a graphical user interface.

## ✨ Features

- Generates a random 6-digit OTP.
- Sends OTP through Gmail SMTP.
- OTP expires after 60 seconds.
- Resend OTP functionality.
- Maximum of 3 verification attempts.
- Secure credential management using environment variables.
- User-friendly GUI built with CustomTkinter.

## 🛠️ Technologies Used

- Python
- CustomTkinter
- SMTP
- Python-dotenv

## 📁 Project Structure

```text
OTP-Verification/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

1. Clone the repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Gmail configuration.
4. Run the application:

```bash
python main.py
```

## 🔒 Security

Never upload your `.env` file or share your Gmail app password.

## 👩‍💻 Author

Saranya
