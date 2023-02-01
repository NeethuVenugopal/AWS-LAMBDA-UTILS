import os
import boto3
import json
from datetime import datetime

client = boto3.client('ses')


def lambda_handler(event, context):
    context = json.loads(json.dumps(event))
    
    email_message = {
        'Body': {
            'Text': {
                'Data': context["content"]
            },
        },
        'Subject': {
            'Data': context["subject"]
        },
    }
    
    print(context["email"],context["subject"] )
    
    ses_response = client.send_email(
        Destination={
            'ToAddresses': [context["email"]],
        },
        Message= email_message,
        Source='info@deepatabc.com'
    )

    print(f"ses response id received: {ses_response['MessageId']}.")