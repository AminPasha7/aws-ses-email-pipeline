# worker/email_worker.py
import boto3, json, time

# Globals (can be overridden by simulator)
sqs = boto3.client("sqs", region_name="us-east-1")
ses = boto3.client("ses", region_name="us-east-1")
QUEUE_URL = "<REPLACE_WITH_SQS_URL>"

def set_clients(sqs_client, ses_client):
    """Allow simulator/tests to inject moto clients."""
    global sqs, ses
    sqs = sqs_client
    ses = ses_client

def set_queue_url(url: str):
    """Allow simulator/tests to inject queue url."""
    global QUEUE_URL
    QUEUE_URL = url

def send_email(p):
    # Works with moto (no real email is sent)
    ses.send_email(
        Source=p["from"],
        Destination={"ToAddresses": p["to"]},
        Message={
            "Subject": {"Data": p["subject"]},
            "Body": {"Text": {"Data": p["body"]}},
        },
    )
    print(f"[OK] Simulated send to {p['to']} | subject='{p['subject']}'")

def process_messages():
    resp = sqs.receive_message(
        QueueUrl=QUEUE_URL, MaxNumberOfMessages=10, WaitTimeSeconds=1
    )
    for m in resp.get("Messages", []):
        try:
            body = json.loads(m["Body"])
            send_email(body)
            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=m["ReceiptHandle"])
        except Exception as e:
            print(f"[ERR] {e}")

if __name__ == "__main__":
    print("Polling SQS… Ctrl+C to stop")
    while True:
        process_messages()
        time.sleep(2)
