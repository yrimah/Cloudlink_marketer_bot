# Cloudlink marketer Bot

Cloudlink marketer Bot is a simple WhatsApp chatbot built with Flask and OpenAI's GPT-3 language model. The bot is designed to handle communication with customers interested in dropshipping products.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your local machine.
- ngrok installed to expose your local server to the internet.
- Meta for developers account with WhatsApp API enabled.
- OpenAI API key.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yrimah/Cloudlink_marketer_bot.git

2. Install dependencies and set up environment variables:

    ```bash
    cd Cloudlink_marketer_bot
    pip install -r requirements.txt

    Create a .env file in the root directory and add the following variables:

    WHAT_TOKEN=<your User WhatsApp API token>
    VERIFY_TOKEN=<your verify token>
    OPENAI_API_KEY=<your OpenAI API key>

3. Run the Flask app:

    ```bash
    python3 main.py

4. Expose the Flask app to the internet using ngrok:

    ```bash
    ngrok http <you app domain name>

5. Copy the ngrok URL and configure it as the webhook URL in your Meta for developers WhatsApp Sandbox settings.

6. Start sending messages to your bot via WhatsApp!
