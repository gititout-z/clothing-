import os
import logging
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Log to console
)
logger = logging.getLogger(__name__)

# Example: You can set different levels for different loggers if needed
# logging.getLogger('twilio').setLevel(logging.WARNING) # To reduce verbosity from libraries

# For production:
# - Log level might be INFO or WARNING, controlled by an environment variable.
# - Handlers might include RotatingFileHandler for file-based logging,
#   or integration with a centralized logging service (e.g., ELK stack, Splunk, CloudWatch Logs).

# In a real production environment, you would configure an actual monitoring service SDK
# (e.g., Sentry, Rollbar) and potentially use environment flags to enable/disable it.
# Example:
# import sentry_sdk
# if os.environ.get("SENTRY_DSN"):
#     sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN"), traces_sample_rate=1.0)


def report_error_to_monitoring_service(exception, context_info=None):
    # In a real production environment, this function would send error details
    # to a monitoring service like Sentry, Rollbar, or AWS CloudWatch.
    # Example:
    # if IS_PRODUCTION_ENV: # A hypothetical flag indicating a production environment
    #     sentry_sdk.capture_exception(exception, extra=context_info)
    logger.error(
        f"MONITORING_HOOK: An error was reported: {type(exception).__name__} - {exception}"
    )
    if context_info:
        logger.error(f"MONITORING_HOOK: Context: {context_info}")


# Placeholder for API credentials - In a real app, use environment variables
# and never hardcode them.
# For more advanced configuration management and validation, consider using Pydantic's BaseSettings:
# from pydantic_settings import BaseSettings
# class Settings(BaseSettings):
#     twilio_account_sid: str
#     twilio_auth_token: str
#     twilio_phone_number: str
#     recipient_phone_number: str
#     class Config:
#         env_file = ".env"
# settings = Settings()
# ACCOUNT_SID = settings.twilio_account_sid

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
    logger.warning("WARN: Twilio creds not set. Using placeholders.")  # noqa: E501
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
        logger.error(f"Error initializing Twilio client: {type(e).__name__} - {e}")
        report_error_to_monitoring_service(
            e, {"details": "Twilio client initialization failed"}
        )
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
        logger.warning("Twilio client not initialized. Cannot send message.")
        logger.debug(f"Intended message to {to} from {from_phone}: {body}")
        return None

    if not all([body, to, from_phone]):
        logger.error(
            "Error: Message body, recipient ('to'), and sender ('from_phone') "
            "are required."
        )
        return None

    try:
        message = client.messages.create(
            body=body, from_=f"whatsapp:{from_phone}", to=f"whatsapp:{to}"
        )
        logger.info(f"Message sent successfully! SID: {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Error sending message: {type(e).__name__} - {e}")
        report_error_to_monitoring_service(
            e,
            {
                "details": "Failed to send WhatsApp message",
                "to": to,
                "body_length": len(body),
            },
        )
        return None


def handle_incoming_message(message_data: dict):
    """
    Placeholder function to process incoming WhatsApp messages.

    Args:
        message_data (dict): The data received from the WhatsApp API
                             (structure depends on the provider).
    """
    try:
        logger.info(f"Received incoming message: {message_data}")
        # IMPORTANT: In a real application, always validate and sanitize
        # data received from external sources like message_data.
        # Example: body = message_data.get('Body', '')
        # if not is_safe_string(body): # Hypothetical validation function
        #     logger.warning(f"Received potentially unsafe input: {body}")
        #     return  # Or handle appropriately
        #
        # Example: Extract message body and sender
        # body = message_data.get('Body')
    except Exception as e:
        logger.error(f"Error processing incoming message: {type(e).__name__} - {e}")
        report_error_to_monitoring_service(
            e,
            {
                "details": "Failed to process incoming WhatsApp message",
                "message_data": message_data,
            },
        )
    # sender = message_data.get('From')
    # if body and sender:
    #     response_message = f"You said: {body}"
    #     send_whatsapp_message(response_message, sender) # Responding back to the sender


if __name__ == "__main__":
    logger.info("Starting WhatsApp application example...")

    # Example: Sending a message (requires RECIPIENT_PHONE_NUMBER to be set)
    if (
        RECIPIENT_PHONE_NUMBER != "RECIPIENT_PHONE_PLACEHOLDER"
        and TWILIO_PHONE_NUMBER != "YOUR_TWILIO_PHONE_PLACEHOLDER"
    ):
        logger.info(
            f"Attempting to send a test message to {RECIPIENT_PHONE_NUMBER} "
            f"from {TWILIO_PHONE_NUMBER}..."
        )
        message_sid = send_whatsapp_message(
            body="Hello from our Python WhatsApp app!",
            to=RECIPIENT_PHONE_NUMBER,
        )
        if message_sid:
            logger.info(f"Test message sent, SID: {message_sid}")
        else:
            logger.warning("Test message sending failed or was simulated.")
    else:
        # fmt: off
        logger.warning("WARN: Recipient/Twilio phone not set. Skip test.")
        # fmt: on
        # fmt: off
        logger.info("To send a test message, set the TWILIO_ACCOUNT_SID, "
                    "TWILIO_AUTH_TOKEN,")  # noqa: E501
        logger.info("TWILIO_PHONE_NUMBER, and RECIPIENT_PHONE_NUMBER "
                    "environment variables.")
        # fmt: on

    # Example: Simulating an incoming message
    logger.info("\nSimulating an incoming message...")
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

    logger.info("\nWhatsApp application example finished.")
