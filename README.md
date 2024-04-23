Here's a README documentation based on the provided code for setting up and running a Discord bot for ELO boosting services. This README includes instructions for initial setup, configuration, and execution.

---

## README: ELO Boosting Discord Bot

### Overview
This Discord bot automates the ELO boosting order process, including ticket detection, order processing, payment handling via Stripe, and management of order assignments and tracking through Google Sheets. Designed primarily for gaming communities on Discord, this bot simplifies transactions and communication between customers and boosters.

### Prerequisites
- Python 3.8 or higher
- Discord account and a server for deployment
- Stripe account for payment processing
- Google account with access to Google Sheets
- Install `nextcord`, `gspread`, `stripe`, `python-dotenv` Python libraries

### Setup Instructions

#### 1. Environment Setup
Install the required Python libraries:
```bash
pip install nextcord gspread stripe python-dotenv oauth2client
```

#### 2. Configuration Files
Create a `.env` file in your project root directory and populate it with the following variables:
```
STRIPE_API_KEY='your_stripe_secret_key'
GOOGLE_SHEETS_CREDENTIALS_PATH='path_to_your_google_service_account_json'
```

#### 3. Google Sheets API Setup
- Create a service account in Google Cloud Platform.
- Download the JSON key file and place it in your project directory.
- Share your Google Sheet with the email address of your service account.

#### 4. Discord Bot Setup
- Create a new application in the Discord Developer Portal.
- Add a bot to the application and copy the bot token.
- Invite the bot to your Discord server with appropriate permissions (e.g., read messages, send messages, manage channels).

#### 5. Config File (`config.json`)
Create a `config.json` file for server-specific settings. Example structure:
```json
{
    "customer_servers": {
        "123456789012345678": {
            "TOKEN": "Your_Discord_Bot_Token",
            "GAME_TYPE": "Type_Of_Game",
            "PRICE_MULTIPLIER": 1.0
        }
    },
    "booster_server": {
        "SERVER_ID": "123456789012345678",
        "CHANNELS": {
            "Type_Of_Game": "channel_id"
        }
    }
}
```
Replace placeholders with actual IDs and values.

### Running the Bot
Execute the bot by running the script:
```bash
python your_script_name.py
```

### Functionalities
- **Automated Ticket Detection**: Monitors Discord channels for new ticket creation with specific prefixes.
- **Order Processing**: Handles customer interactions within Discord for selecting ELO boosts and generates Stripe payment links.
- **Booster Assignment**: Manages booster profiles and assigns boosters to orders automatically.
- **Google Sheets Integration**: Updates a Google Sheet in real time with order details, payments, and assignment tracking.

### Additional Notes
- Ensure the bot has the necessary permissions on your Discord server to read and send messages.
- The system should be monitored for any operational issues or bugs that may affect processing or user experience.

---

This README should provide a comprehensive guide to setting up and operating the ELO boosting Discord bot. Adjust paths, tokens, and other configurations as necessary to suit your environment and security practices.