from module import *

load_dotenv()

STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
stripe.api_key = STRIPE_API_KEY

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