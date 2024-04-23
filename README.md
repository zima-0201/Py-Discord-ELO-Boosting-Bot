# ELO Boost Bot

ELO Boost Bot is a Discord bot designed to automate order processing, payment handling, and booster assignment for a gaming ELO boosting service. This project integrates multiple APIs, including Discord, Stripe, and Google Sheets, to provide a seamless and automated service from ticket creation to order completion.

## Video Preview

[![Video Preview](https://github.com/zima-0201/Project-Images/blob/main/video%20preview/Py-Discord-ELO-Boosting-Bot.png)](https://brand-car.s3.eu-north-1.amazonaws.com/Four+Seasons/Py-Discord-ELO-Boosting-Bot.mp4)


## Features

- **Automated Ticket Detection**: Detects new orders through specific Discord channels.
- **Order Processing**: Processes user inputs and generates Stripe payment links automatically.
- **Automatic Booster Assignment**: Assigns boosters based on predefined criteria and their availability.
- **Google Sheets Integration**: Updates a Google Sheet in real-time with order details and status.
- **Secure Payment Processing**: Integrates with Stripe for secure online payments.

## Technology Stack

- **Backend**: Python with discord.py
- **Database**: MongoDB for storing booster profiles and order details
- **APIs**:
  - Discord API for bot interaction
  - Stripe API for payment processing
  - Google Sheets API for data logging and tracking

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

```bash
python -m pip install nextcord gspread stripe python-dotenv
```

You will also need to set up Stripe and Google Cloud service accounts and download the necessary credentials files, setting them as environment variables or directly within your configuration files.

### Installing

A step-by-step series of examples that tell you how to get a development env running:

1. Clone the repository:
   ```bash
   git clone https://yourrepositorylink.com
   ```
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables for your Stripe API key and Google Sheets credentials path:
   ```bash
   export STRIPE_API_KEY='your_stripe_api_key_here'
   export GOOGLE_SHEETS_CREDENTIALS_PATH='path_to_your_google_sheets_credentials.json'
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## Configuration

Explain how to configure the bot, including where to place and how to format the `config.json` file.

## Usage

Detail how to interact with the bot, including commands and expected responses. For example:

- `!order [current_rank] [desired_rank] [region] [streaming] [choose_agents]`: Starts the order process.
- `!price [current_rank] [desired_rank]`: Provides a price quote for the specified ELO boost.

## Contributing

Please read [CONTRIBUTING.md](LINK_TO_YOUR_CONTRIBUTING.MD) for details on our code of conduct, and the process for submitting pull requests to us.
