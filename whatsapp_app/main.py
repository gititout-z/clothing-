import os
from twilio.rest import Client

# Placeholder for API credentials - In a real app, use environment variables
# and never hardcode them.
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "YOUR_ACCOUNT_SID_PLACEHOLDER")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "YOUR_AUTH_TOKEN_PLACEHOLDER")
TWILIO_PHONE_NUMBER = os.environ.get(
    "TWILIO_PHONE_NUMBER", "YOUR_TWILIO_PHONE_PLACEHOLDER"
)
RECIPIENT_PHONE_NUMBER = os.environ.get(
    "RECIPIENT_PHONE_NUMBER", "RECIPIENT_PHONE_PLACEHOLDER"
)  # For sending test messages

# Initialize the Twilio client
# In a real scenario, you'd want to handle potential errors during client initialization.
if (
    ACCOUNT_SID == "YOUR_ACCOUNT_SID_PLACEHOLDER"
    or AUTH_TOKEN == "YOUR_AUTH_TOKEN_PLACEHOLDER"
):
    # fmt: off
    print(
        "WARN: Twilio creds not set. Using placeholders."
    )
    # fmt: on
    # You might use a mock client here for local development if the library
    # supports it, or skip client initialization if it would cause an error
    # with placeholders.
    # For now, we'll proceed, but actual API calls will fail.
    client = None
else:
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
    except Exception as e:
        print(f"Error initializing Twilio client: {type(e).__name__} - {e}")
        client = None


def send_whatsapp_message(body: str, to: str, from_phone: str = TWILIO_PHONE_NUMBER):
    """
    Sends a WhatsApp message using Twilio.

    Args:
        body (str): The content of the message.
        to (str): The recipient's WhatsApp number (e.g., 'whatsapp:+14155238886').
        from_phone (str): The Twilio WhatsApp-enabled phone number
                          (e.g., 'whatsapp:+14155238886').
                          Defaults to TWILIO_PHONE_NUMBER.
    Returns:
        str: The message SID if successful, None otherwise.
    """
    if not client:
        print("Twilio client not initialized. Cannot send message.")
        print(f"Intended message to {to} from {from_phone}: {body}")
        return None

    if not all([body, to, from_phone]):
        print(
            "Error: Message body, recipient ('to'), and sender ('from_phone') "
            "are required."
        )
        return None

    try:
        message = client.messages.create(
            body=body, from_=f"whatsapp:{from_phone}", to=f"whatsapp:{to}"
        )
        print(f"Message sent successfully! SID: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"Error sending message: {type(e).__name__} - {e}")
        return None


def handle_incoming_message(message_data: dict):
    """
    Placeholder function to process incoming WhatsApp messages.

    Args:
        message_data (dict): The data received from the WhatsApp API
                             (structure depends on the provider).
    """
    try:
        print(f"Received incoming message: {message_data}")
        # Example: Extract message body and sender
        # body = message_data.get('Body')
    except Exception as e:
        print(f"Error processing incoming message: {type(e).__name__} - {e}")
    # sender = message_data.get('From')
    # if body and sender:
    #     response_message = f"You said: {body}"
    #     send_whatsapp_message(response_message, sender) # Responding back to the sender


if __name__ == "__main__":
    print("Starting WhatsApp application example...")

    # Example: Sending a message (requires RECIPIENT_PHONE_NUMBER to be set)
    if (
        RECIPIENT_PHONE_NUMBER != "RECIPIENT_PHONE_PLACEHOLDER"
        and TWILIO_PHONE_NUMBER != "YOUR_TWILIO_PHONE_PLACEHOLDER"
    ):
        print(
            f"Attempting to send a test message to {RECIPIENT_PHONE_NUMBER} "
            f"from {TWILIO_PHONE_NUMBER}..."
        )
        message_sid = send_whatsapp_message(
            body="Hello from our Python WhatsApp app!",
            to=RECIPIENT_PHONE_NUMBER,
        )
        if message_sid:
            print(f"Test message sent, SID: {message_sid}")
        else:
            print("Test message sending failed or was simulated.")
    else:
        # fmt: off
        print(
            "WARN: Recipient/Twilio phone not set. Skip test."
        )
        # fmt: on
        print(
            "To send a test message, set the TWILIO_ACCOUNT_SID, "
            "TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, and "
            "RECIPIENT_PHONE_NUMBER environment variables."
        )

    # Example: Simulating an incoming message
    print("\nSimulating an incoming message...")
    sample_incoming_message = {
        "SmsMessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NumMedia": "0",
        "SmsSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "SmsStatus": "received",
        "Body": "Hello there!",
        "To": f"whatsapp:{TWILIO_PHONE_NUMBER}",
        "NumSegments": "1",
        "MessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "AccountSid": ACCOUNT_SID,
        # Simulating incoming from recipient
        "From": f"whatsapp:{RECIPIENT_PHONE_NUMBER}",
        "ApiVersion": "2010-04-01",
    }
    handle_incoming_message(sample_incoming_message)

    print("\nWhatsApp application example finished.")
