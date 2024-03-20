
def calculate_delivery_fee(city):
    if city == "dhaka":
        return 100
    elif city == "outside-dhaka":
        return 120
    else:
        return 0  # Default value or handle other cases as needed
