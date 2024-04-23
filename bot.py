from module import *
from calculate import calculate_price
from payment import create_stripe_payment_link

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

        # Send the response back to the user in the channel
        await interaction.response.send_message(description, ephemeral=True)

        # Send information to the appropriate booster server channel based on the game type
        booster_guild = client.get_guild(int(config['booster_server']['SERVER_ID']))
        booster_channel_id = config['booster_server']['CHANNELS'][game_type]
        booster_channel = booster_guild.get_channel(int(booster_channel_id))
        if booster_channel:
            await booster_channel.send(description)

    client.run(token)