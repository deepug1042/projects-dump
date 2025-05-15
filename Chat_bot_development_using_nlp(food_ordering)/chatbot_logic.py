MENU = {
    "idli": 30,
    "dosa": 40,
    "vada": 25,
    "uttapam": 50,
    "pongal": 45,
    "upma": 35,
    "sambar rice": 55
}

def get_bot_response(user_input, session):
    stage = session.get("stage", "greeting")
    user_input = user_input.lower()

    if stage == "greeting":
        session["stage"] = "get_name"
        return "Hi there! Welcome to South Spice! What's your name?"

    elif stage == "get_name":
        session["user"]["name"] = user_input.title()
        session["stage"] = "get_phone"
        return f"Nice to meet you, {session['user']['name']}! Please enter your phone number."

    elif stage == "get_phone":
        session["user"]["phone"] = user_input
        session["stage"] = "menu"
        menu_str = "\n".join([f"{item.title()}: ₹{price}" for item, price in MENU.items()])
        return f"Here's our menu:\n{menu_str}\nPlease type your order items separated by commas."

    elif stage == "menu":
        items = [item.strip().lower() for item in user_input.split(",")]
        order = []
        total = 0
        for item in items:
            if item in MENU:
                order.append((item.title(), MENU[item]))
                total += MENU[item]
        if order:
            session["order"] = order
            session["total"] = total
            session["stage"] = "confirm"
            order_summary = "\n".join([f"{item}: ₹{price}" for item, price in order])
            return f"Please confirm your order:\n{order_summary}\nTotal: ₹{total}\nType 'yes' to confirm."
        return "Sorry, some items were not recognized. Please try again."

    elif stage == "confirm":
        if "yes" in user_input:
            session["stage"] = "payment"
            return "Thank you! Redirecting you to the payment page in 10 seconds..."
        else:
            session["stage"] = "menu"
            return "Okay, please re-enter your order."

    elif stage == "done":
        return "You’ve already placed your order. Your food will arrive shortly!"

    return "I didn’t quite get that. Can you try again?"
