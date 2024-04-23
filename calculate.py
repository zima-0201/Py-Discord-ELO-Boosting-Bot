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