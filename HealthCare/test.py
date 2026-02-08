
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMessage(Username, Password, receiveremail):
    sender_email = "websiteyash@gmail.com"  # Your email address
    receiver_email = receiveremail  # Recipient's email address
    subject = "Welcome to Our Service"

    # HTML Email Template with dynamic username & password
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Our Service</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
            .header {{ background: #2d47d5; color: white; padding: 20px; text-align: center; font-size: 24px; border-radius: 8px 8px 0 0; }}
            .content {{ padding: 20px; text-align: center; color: #343a40; }}
            .content h2 {{ color: #2d47d5; }}
            .test-card {{ background: #2d47d5; color: white; padding: 15px; border-radius: 8px; margin-top: 20px; }}
            .footer {{ padding: 15px; background: #ddd; text-align: center; font-size: 14px; border-radius: 0 0 8px 8px; }}
            .action-button {{ background: #2d47d5; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Welcome, {Username}!</div>
            <div class="content">
                <h2>Thank you for signing up!</h2>
                <p>Your login details:</p>
                <div class="test-card">
                    <h3>Username: {Username}</h3>
                    <h3>Password: {Password}</h3>
                </div>
                <p>Click below to log in:</p>
                <a href="https://yourwebsite.com/login" class="action-button">Login Now</a>
            </div>
            <div class="footer">&copy; 2025 Your Company. All rights reserved.</div>
        </div>
    </body>
    </html>
    """
      # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'html'))  # Attach HTML content

    # Gmail SMTP Server
    gmail_password = "gspl bdsf qwde ksgp"

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure connection
            server.login(sender_email, gmail_password)  # Log in
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Send email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


sendMessage("TestUser", "secure123", "websiteyash@gamil.com")
