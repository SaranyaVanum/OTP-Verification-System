import customtkinter as ctk
import random
import smtplib
import re
import os

from email.message import EmailMessage
from dotenv import load_dotenv
from tkinter import messagebox
from datetime import datetime

# ==========================
# LOAD ENVIRONMENT VARIABLES
# ==========================

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# ==========================
# GLOBAL VARIABLES
# ==========================

current_otp = ""
time_left = 60
timer_running = False
attempts_left = 3
otp_visible = False

# ==========================
# SAVE LOG
# ==========================

def save_log(email, status):
    with open("logs.txt", "a") as file:
        file.write("=" * 45 + "\n")
        file.write(f"Date : {datetime.now()}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Status: {status}\n")
        file.write("=" * 45 + "\n\n")

# ==========================
# EMAIL VALIDATION
# ==========================

def valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)

# ==========================
# OTP GENERATOR
# ==========================

def generate_otp():
    return str(random.randint(100000,999999))

# ==========================
# SHOW / HIDE OTP
# ==========================

def toggle_otp():

    global otp_visible

    if otp_visible:
        otp_entry.configure(show="*")
        eye_btn.configure(text="👁")
        otp_visible=False

    else:
        otp_entry.configure(show="")
        eye_btn.configure(text="🙈")
        otp_visible=True

# ==========================
# TIMER
# ==========================

def update_timer():

    global time_left
    global timer_running
    global current_otp

    if timer_running:

        mins=time_left//60
        secs=time_left%60

        timer_label.configure(
            text=f"⏳ OTP expires in : {mins:02}:{secs:02}"
        )

        if time_left>0:

            time_left-=1
            app.after(1000,update_timer)

        else:

            timer_running=False
            current_otp=""

            timer_label.configure(
                text="❌ OTP Expired!",
                text_color="red"
            )

            resend_btn.configure(
                state="normal",
                fg_color="#FF8C00",
                hover_color="#E67E00"
            )

# ==========================
# SEND OTP
# ==========================

def send_otp():

    global current_otp
    global time_left
    global timer_running
    global attempts_left

    receiver=email_entry.get().strip()

    if receiver=="":

        status_label.configure(
            text="❌ Please enter your email.",
            text_color="red"
        )
        return

    if not valid_email(receiver):

        status_label.configure(
            text="❌ Invalid Email Address",
            text_color="red"
        )
        return

    current_otp=generate_otp()

    attempts_left=3

    attempt_label.configure(
        text=f"Attempts Left : {attempts_left}"
    )

    resend_btn.configure(
        state="disabled",
        fg_color="#808080",
        hover_color="#808080"
    )

    time_left=60
    timer_running=True

    update_timer()

    try:

        msg=EmailMessage()

        msg["Subject"]="SecureMail Verification OTP"

        msg["From"]=EMAIL

        msg["To"]=receiver

        msg.set_content(f"""

Hello,

Your One-Time Password (OTP) is:

{current_otp}

This OTP will expire in 60 seconds.

Do not share this OTP with anyone.

Regards,

SecureMail Verify
""")

        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:

            smtp.login(
                EMAIL,
                APP_PASSWORD
            )

            smtp.send_message(msg)

        save_log(receiver,"OTP Sent")

        status_label.configure(
            text="✅ OTP Sent Successfully!",
            text_color="green"
        )

    except Exception as e:

        status_label.configure(
            text="❌ Failed to Send OTP",
            text_color="red"
        )

        print(e)

# ==========================
# VERIFY OTP
# ==========================

def verify_otp():
        global attempts_left
        global current_otp
        global timer_running

        entered_otp = otp_entry.get().strip()
        receiver = email_entry.get().strip()

        if entered_otp == "":
            status_label.configure(
                text="❌ Please enter the OTP.",
                text_color="red"
            )
            return

        if current_otp == "":
            status_label.configure(
                text="❌ OTP Expired! Please resend OTP.",
                text_color="red"
            )
            return

        if entered_otp == current_otp:

            timer_running = False

            save_log(receiver, "OTP Verified Successfully")

            status_label.configure(
                text="✅ Email Verified Successfully!",
                text_color="green"
            )

            messagebox.showinfo(
                "Verification Successful",
                f"🎉 Welcome!\n\n{receiver}\n\nYour email has been verified successfully."
            )

            email_entry.delete(0, "end")
            otp_entry.delete(0, "end")

            timer_label.configure(
                text="⏳ OTP expires in : --:--",
                text_color="orange"
            )

            resend_btn.configure(
                state="disabled",
                fg_color="#808080",
                hover_color="#808080"
            )

            current_otp = ""

        else:

            attempts_left -= 1

            attempt_label.configure(
                text=f"Attempts Left : {attempts_left}"
            )

            save_log(receiver, "Incorrect OTP")

            if attempts_left == 0:

                current_otp = ""
                timer_running = False

                status_label.configure(
                    text="❌ Maximum Attempts Reached!",
                    text_color="red"
                )

                resend_btn.configure(
                    state="normal",
                    fg_color="#FF8C00",
                    hover_color="#E67E00"
                )

            else:

                status_label.configure(
                    text=f"❌ Incorrect OTP! ({attempts_left} Attempts Left)",
                    text_color="red"
                )

# ==========================
# GUI
# ==========================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x720")
app.resizable(False, False)

# ==========================
# APP BACKGROUND
# ==========================

app.configure(fg_color="#101827")

app.title("🔐 SecureMail Verify")
app.geometry("700x720")
app.resizable(False, False)

title = ctk.CTkLabel(
    app,
    text="🔐 SecureMail Verify",
    font=("Segoe UI", 34, "bold"),
    text_color="#4EA8FF",
    fg_color="transparent"
)
title.pack(pady=(25,5))

subtitle = ctk.CTkLabel(
    app,
    text="Professional Email Authentication System",
    font=("Segoe UI",16),
    text_color="white",
    fg_color="transparent"
)
subtitle.pack(pady=(0,25))

email_label = ctk.CTkLabel(
    app,
    text="📧 Email Address",
    font=("Segoe UI",16,"bold"),
    fg_color="transparent"
)
email_label.pack(anchor="w", padx=90)

email_entry = ctk.CTkEntry(
    app,
    width=500,
    height=45,
    corner_radius=12,
    placeholder_text="Enter your email..."
)
email_entry.pack(pady=10)

send_btn = ctk.CTkButton(
    app,
    text="📩 Send OTP",
    width=240,
    height=45,
    corner_radius=15,
    font=("Segoe UI",16,"bold"),
    command=send_otp
)
send_btn.pack(pady=20)

otp_label = ctk.CTkLabel(
    app,
    text="🔢 Verification Code",
    font=("Segoe UI",16,"bold"),
    fg_color="transparent"
)
otp_label.pack(anchor="w", padx=90)

otp_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
otp_frame.pack()

otp_entry = ctk.CTkEntry(
    otp_frame,
    width=430,
    height=45,
    corner_radius=12,
    placeholder_text="Enter 6-digit OTP",
    show="*"
)
otp_entry.pack(side="left", padx=(0,10))

eye_btn = ctk.CTkButton(
    otp_frame,
    text="👁",
    width=50,
    command=toggle_otp
)
eye_btn.pack(side="left")

verify_btn = ctk.CTkButton(
    app,
    text="✅ Verify OTP",
    width=240,
    height=45,
    corner_radius=15,
    font=("Segoe UI",16,"bold"),
    fg_color="#2E8B57",
    hover_color="#256F49",
    command=verify_otp
)
verify_btn.pack(pady=20)
# ==========================
# RESEND BUTTON
# ==========================

resend_btn = ctk.CTkButton(
    app,
    text="🔄 Resend OTP",
    command=send_otp,
    width=240,
    height=45,
    corner_radius=15,
    font=("Segoe UI",16,"bold"),
    fg_color="#808080",
    hover_color="#808080",
    state="disabled"
)
resend_btn.pack(pady=10)

# ==========================
# TIMER LABEL
# ==========================

timer_label = ctk.CTkLabel(
    app,
    text="⏳ OTP expires in: --:--",
    font=("Segoe UI",15,"bold"),
    text_color="orange",
    fg_color="transparent"
)
timer_label.pack(pady=15)

# ==========================
# ATTEMPTS LABEL
# ==========================

attempt_label = ctk.CTkLabel(
    app,
    text="Attempts Left : 3",
    font=("Segoe UI",15,"bold"),
    text_color="#FFD166",
    fg_color="transparent"
)
attempt_label.pack()

# ==========================
# STATUS LABEL
# ==========================

status_label = ctk.CTkLabel(
    app,
    text="",
    fg_color="transparent"
)
status_label.pack(pady=20)

# ==========================
# FOOTER
# ==========================

footer = ctk.CTkLabel(
    app,
    text="Powered by Python ❤️ | SecureMail Verify v2.0",
    font=("Segoe UI",12),
    text_color="gray"
)
footer.pack(side="bottom", pady=15)

# ==========================
# START APPLICATION
# ==========================

app.mainloop()