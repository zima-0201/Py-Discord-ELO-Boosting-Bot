from module import *

from bot import bot_task
from payment import create_stripe_payment_link

load_dotenv()

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
