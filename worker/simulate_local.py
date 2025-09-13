# worker/simulate_local.py
import json, boto3
from moto import mock_aws

from email_worker import process_messages, set_clients, set_queue_url

@mock_aws
def main():
    # Create mocked AWS clients
    sqs = boto3.client("sqs", region_name="us-east-1")
    ses = boto3.client("ses", region_name="us-east-1")
    sns = boto3.client("sns", region_name="us-east-1")

    # Create fake resources
    q = sqs.create_queue(QueueName="job-alert-queue")
    queue_url = q["QueueUrl"]

    # Fake SES identity verification so send_email doesn't error
    ses.verify_email_identity(EmailAddress="alerts@demo.com")

    # Inject mocked clients + queue URL into worker
    set_clients(sqs, ses)
    set_queue_url(queue_url)

    # Push a test message
    msg = {
        "from": "alerts@demo.com",
        "to": ["user@example.com"],
        "subject": "Test Job Alert",
        "body": "This is a simulated job alert using Moto (no AWS usage).",
    }
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(msg))

    print("Running local simulation (Moto)…")
    process_messages()
    print("Simulation complete ✅")

if __name__ == "__main__":
    main()
