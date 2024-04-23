import os
import json
import nextcord
import gspread
import stripe
from nextcord.ext import commands
from nextcord import Interaction, Embed, SlashOption
from dotenv import load_dotenv
from multiprocessing import Process, freeze_support
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

load_dotenv()

STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
stripe.api_key = STRIPE_API_KEY
print(STRIPE_API_KEY)

# Load Google Sheets credentials from environment variable
google_credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
if not google_credentials_path:
    raise ValueError("The Google Sheets credentials path is not set in the environment variables")

# Set the scope and credentials for Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_path, scope)
client = gspread.authorize(creds)

# Open the Google Spreadsheet by title
sheet_url = "https://docs.google.com/spreadsheets/d/1ImUhNYctOUVSLtdktvzsnd8zkpzVDedPYhSix7CRg8c/edit?usp=sharing"
spreadsheet = client.open_by_url(sheet_url)

worksheet_name = "Sheet1"
worksheet = spreadsheet.get_worksheet(0)

# If the worksheet is not found, create a new one
if worksheet is None:
    worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

# Define the header names
header_names = [
    "Customer Discord ID",
    "Global Order ID",
    "Stripe Payment ID",
    "Customer Payment",
    "Booster Payout",
    "Order Details",
    "Order Status",
    "Booster ID on the Order",
    "Date of Order",
    "Date Order was Completed"
]

# Check if the worksheet is empty (no header row) and add headers if needed
existing_headers = worksheet.row_values(1)
if not existing_headers:
    worksheet.insert_row(header_names, index=1)

def calculate_price(current_rank, desired_rank, price_multiplier):
    # Updated price base to reflect more detailed ranks
    price_base = {
        'Iron 1': 50, 'Iron 2': 55, 'Iron 3': 60,
        'Bronze 1': 65, 'Bronze 2': 70, 'Bronze 3': 75,
        'Silver 1': 80, 'Silver 2': 85, 'Silver 3': 90,
        'Gold 1': 95, 'Gold 2': 100, 'Gold 3': 105,
        'Platinum 1': 110, 'Platinum 2': 115, 'Platinum 3': 120,
        'Diamond 1': 125, 'Diamond 2': 130, 'Diamond 3': 135,
        'Ascendant 1': 140, 'Ascendant 2': 145, 'Ascendant 3': 150,
        'Immortal 1': 155, 'Immortal 2': 160, 'Immortal 3': 165
    }

    # Calculate price based on the rank values and the multiplier
    # Ensure both ranks exist in the dictionary to avoid KeyError
    if current_rank in price_base and desired_rank in price_base:
        # Calculate the price difference based on rank values
        price_diff = price_base[desired_rank] - price_base[current_rank]
        # Apply the multiplier to the price difference
        return max(0, price_diff * price_multiplier)  # Ensure price does not go negative
    else:
        # Return a default or error if ranks are not found
        return None  # You could also raise an exception or handle this case differently

async def create_stripe_payment_link(amount):
    try:
        # Convert amount to cents or use the smallest currency unit
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # converting dollars to cents
            currency='usd',
            payment_method_types=['card'],
        )
        return payment_intent.payment_url
    except Exception as e:
        print(f"Failed to create payment intent: {str(e)}")
        return None

def bot_task(server_id, token, game_type, price_multiplier):
    global config
    with open('config.json', 'r') as f:
        config = json.load(f)

    intents = nextcord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.guilds = True

    client = commands.Bot(command_prefix="!", intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user} on server {server_id}')

    @client.slash_command(name="order")
    async def order_command(
        interaction: Interaction,
        current_rank: str = SlashOption(
            required=True, 
            choices=[
                "Iron 1", "Iron 2", "Iron 3",
                "Bronze 1", "Bronze 2", "Bronze 3",
                "Silver 1", "Silver 2", "Silver 3",
                "Gold 1", "Gold 2", "Gold 3",
                "Platinum 1", "Platinum 2", "Platinum 3",
                "Diamond 1", "Diamond 2", "Diamond 3",
                "Ascendant 1", "Ascendant 2", "Ascendant 3",
                "Immortal 1", "Immortal 2", "Immortal 3"
            ]
        ),
        desired_rank: str = SlashOption(
            required=True,
            choices=[
                "Iron 1", "Iron 2", "Iron 3",
                "Bronze 1", "Bronze 2", "Bronze 3",
                "Silver 1", "Silver 2", "Silver 3",
                "Gold 1", "Gold 2", "Gold 3",
                "Platinum 1", "Platinum 2", "Platinum 3",
                "Diamond 1", "Diamond 2", "Diamond 3",
                "Ascendant 1", "Ascendant 2", "Ascendant 3",
                "Immortal 1", "Immortal 2", "Immortal 3"
            ]
        ),
        region: str = SlashOption(required=True, choices=["NA", "EU", "ASIA"]),
        streaming: bool = SlashOption(required=False),
        choose_agents: bool = SlashOption(required=False)
    ):
        # Check if the command is used in the correct channel
        if not interaction.channel.name.startswith("order-"):
            await interaction.response.send_message("⚠️ This command can only be used in 'order-' channels.", ephemeral=True)
            return

        # Calculate the price based on the current and desired rank
        price_multiplier = config['customer_servers'][str(interaction.guild.id)]['PRICE_MULTIPLIER']
        price = calculate_price(current_rank, desired_rank, price_multiplier)

        # Construct the description for the order summary
        game_type = config['customer_servers'][str(interaction.guild.id)]['GAME_TYPE']
        description = (
            f"**Game Type:** {game_type}\n"
            f"**Current Rank:** {current_rank}\n"
            f"**Desired Rank:** {desired_rank}\n"
            f"**Region:** {region}\n"
            f"**Streaming:** {'Yes' if streaming else 'No'}\n"
            f"**Choose Agents:** {choose_agents if choose_agents else 'Not specified'}\n"
            f"**Price:** ${price}"
        )
        payment_url = await create_stripe_payment_link(1)
        print(payment_url) 
        # Send the response back to the user in the channel
        await interaction.response.send_message(payment_url, ephemeral=True)

        # Send information to the appropriate booster server channel based on the game type
        booster_guild = client.get_guild(int(config['booster_server']['SERVER_ID']))
        booster_channel_id = config['booster_server']['CHANNELS'][game_type]
        booster_channel = booster_guild.get_channel(int(booster_channel_id))
        if booster_channel:
            await booster_channel.send(description)

    @client.slash_command(name="price", description="Get a price quote for an ELO boost")
    async def price_command(
        interaction: Interaction,
        current_rank: str = SlashOption(
            required=True, 
            choices=[
                "Iron 1", "Iron 2", "Iron 3",
                "Bronze 1", "Bronze 2", "Bronze 3",
                "Silver 1", "Silver 2", "Silver 3",
                "Gold 1", "Gold 2", "Gold 3",
                "Platinum 1", "Platinum 2", "Platinum 3",
                "Diamond 1", "Diamond 2", "Diamond 3",
                "Ascendant 1", "Ascendant 2", "Ascendant 3",
                "Immortal 1", "Immortal 2", "Immortal 3"
            ]
        ),
        desired_rank: str = SlashOption(
            required=True,
            choices=[
                "Iron 1", "Iron 2", "Iron 3",
                "Bronze 1", "Bronze 2", "Bronze 3",
                "Silver 1", "Silver 2", "Silver 3",
                "Gold 1", "Gold 2", "Gold 3",
                "Platinum 1", "Platinum 2", "Platinum 3",
                "Diamond 1", "Diamond 2", "Diamond 3",
                "Ascendant 1", "Ascendant 2", "Ascendant 3",
                "Immortal 1", "Immortal 2", "Immortal 3"
            ]
        )
    ):
        # Check if the command is used in the correct channel
        if not interaction.channel.name.startswith("order-"):
            await interaction.response.send_message("⚠️ This command can only be used in 'order-' channels.", ephemeral=True)
            return

        # Calculate the price based on the current and desired rank
        price_multiplier = config['customer_servers'][str(interaction.guild.id)]['PRICE_MULTIPLIER']
        price = calculate_price(current_rank, desired_rank, price_multiplier)

        # Construct the description for the order summary
        game_type = config['customer_servers'][str(interaction.guild.id)]['GAME_TYPE']
        description = f"The price for boosting from {current_rank} to {desired_rank} is ${price}"

        payment_url = await create_stripe_payment_link(price)
        print(payment_url)

        # Send the response back to the user in the channel
        await interaction.response.send_message(description, ephemeral=True)
        
        # Send information to the appropriate booster server channel based on the game type
        booster_guild = client.get_guild(int(config['booster_server']['SERVER_ID']))
        booster_channel_id = config['booster_server']['CHANNELS'][game_type]
        booster_channel = booster_guild.get_channel(int(booster_channel_id))
        if booster_channel:
            await booster_channel.send(description)

    client.run(token)

if __name__ == '__main__':
    freeze_support()  # For Windows support
    # Load the configuration file
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Create and start a separate process for each bot
    processes = []
    for server_id, details in config['customer_servers'].items():
        p = Process(target=bot_task, args=(server_id, details['TOKEN'], details['GAME_TYPE'], details['PRICE_MULTIPLIER']))
        p.start()
        processes.append(p)

    # Optionally join processes
    for process in processes:
        process.join()
