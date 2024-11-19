import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()
 
sender_email = os.getenv('SENDER_EMAIL')
password= os.getenv('EMAIL_PASS')

print(sender_email,password)

# Email credentials

def send_email(receiver_email, subject, body):
    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Sending the email
    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Upgrade to a secure connection
        server.login(sender_email, password)  # Login to the SMTP server
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
        return { 'message' : 'Email sent successfully!'}
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()
