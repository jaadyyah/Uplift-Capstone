import boto3, botocore
from email_validator import EmailNotValidError, validate_email
ses = boto3.client("ses", region_name="us-east-1")

def send_email(user_email, subject, body):
    try:
        email_to_send = validate_email(user_email, check_deliverability=True)
    except EmailNotValidError as email_err:
        print("Email is invalid and will not be sent:", email_err)
        return False
    try:
        ses.send_email(
            Source="Uplift Company <mail@upliftcompanyusa.com>",
            Destination={"ToAddresses": [email_to_send.email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}}
            }
        )
        print(f"Sent email successfully: {email_to_send.email}")
        return True
    except botocore.exceptions.BotoCoreError as err:
        print("Attempted to send email and failed:", err)
        return False