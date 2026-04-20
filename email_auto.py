import boto3
ses = boto3.client("ses", region_name="us-east-1")

def send_email(user_email, body):
    return ses.send_email(
        Source="mail@upliftcompanyusa.com",
        Destination={"ToAddresses": ["upliftcomapny123@gmail.com"]},
        Message={
            "Subject": {"Data": "Hello"},
            "Body": {"Text": {"Data": body}}
        }
    )