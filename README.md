# Python WhatsApp Application Starter

This project is a starter template for building Python applications that integrate with WhatsApp, for example, using the Twilio API. It provides a basic structure, example code, unit tests, linting, formatting, and pre-commit hooks to ensure code quality.

## Project Purpose

The primary goal is to provide a foundation for developing WhatsApp bots, notification systems, or other applications that leverage WhatsApp messaging. The example code demonstrates sending a message and a placeholder for handling incoming messages via Twilio.

## Setup Instructions

### 1. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
The application uses environment variables for API credentials and phone numbers. Create a `.env` file in the project root (and ensure `.env` is in your `.gitignore` file, which it should be by default) or set these variables in your environment:

```env
TWILIO_ACCOUNT_SID="YOUR_ACTUAL_ACCOUNT_SID"         # Replace with your Twilio Account SID
TWILIO_AUTH_TOKEN="YOUR_ACTUAL_AUTH_TOKEN"          # Replace with your Twilio Auth Token
TWILIO_PHONE_NUMBER="YOUR_TWILIO_WHATSAPP_NUMBER"   # Your Twilio WhatsApp-enabled number, e.g., +14155238886
RECIPIENT_PHONE_NUMBER="RECIPIENT_WHATSAPP_NUMBER" # A WhatsApp number to send test messages to, e.g., +14155238886
```
**Important:** Never commit your actual credentials to version control. The example code uses placeholders if these are not set, but API calls will not succeed.

## Running the Application
To run the example application:
```bash
python whatsapp_app/main.py
```
This will attempt to send a test message if `RECIPIENT_PHONE_NUMBER` and Twilio credentials are configured, and simulate an incoming message.

## Running Tests
To run the unit tests:
```bash
python -m pytest
```

## Code Quality

This project uses `black` for code formatting and `flake8` for linting.

To format the code:
```bash
python -m black .
```

To check for linting issues:
```bash
python -m flake8 .
```

### Pre-commit Hooks
Pre-commit hooks are configured to automatically run `black` and `flake8` before each commit. To enable them:
1. Install pre-commit (if not already installed with `requirements.txt`, though it's good practice to list dev tools there or in a `requirements-dev.txt`):
   ```bash
   pip install pre-commit
   ```
2. Set up the hooks:
   ```bash
   pre-commit install
   ```
You can also run them manually on all files:
```bash
pre-commit run --all-files
```

## Further Documentation
More detailed documentation regarding specific modules or advanced configuration can be added to the `docs/` directory.
