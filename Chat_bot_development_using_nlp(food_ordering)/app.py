from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=10)

# Menu items
MENU = {
    "dosa": 40,
    "idli": 30,
    "vada": 35,
    "upma": 30,
    "pongal": 50
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'messages' not in session:
        session['messages'] = []
        session['state'] = 'greet'
        session['user_info'] = {}
        session['order'] = []

    if request.method == 'POST':
        user_input = request.form['message']
        session['messages'].append(('user', user_input))

        if session.get('state') == 'done':
            if 'yes' in user_input.lower():
                session['messages'] = []
                session['state'] = 'greet'
                session['user_info'] = {}
                session['order'] = []
            else:
                session['messages'].append(('bot', "Alright! Feel free to return anytime. 👋"))
                return redirect(url_for('index'))

        response = handle_conversation(user_input)
        if response:
            session['messages'].append(('bot', response))
        session.modified = True

    return render_template('chat.html', messages=session.get('messages'))

def handle_conversation(user_input):
    state = session.get('state')
    user_input = user_input.lower()
    user_info = session.get('user_info')
    order = session.get('order')

    if state == 'greet':
        session['state'] = 'ask_name'
        return "Hi there! I'm FoodieBot. What's your name?"

    elif state == 'ask_name':
        user_info['name'] = user_input.title()
        session['state'] = 'ask_number'
        return f"Nice to meet you, {user_info['name']}! Could you share your phone number?"

    elif state == 'ask_number':
        user_info['phone'] = user_input
        session['state'] = 'show_menu'
        menu_str = "\n".join([f"{item.title()} - ₹{price}" for item, price in MENU.items()])
        return f"Thanks! Here's our South Indian menu:\n{menu_str}\n\nPlease enter the items you want to order (separated by commas)."

    elif state == 'show_menu':
        items = [item.strip().lower() for item in user_input.split(',')]
        order.clear()
        invalid_items = []
        for item in items:
            if item in MENU:
                order.append((item.title(), MENU[item]))
            else:
                invalid_items.append(item)

        if order:
            summary = "\n".join([f"{item} - ₹{price}" for item, price in order])
            total = sum(price for _, price in order)
            session['state'] = 'confirm_order'
            return f"Here's your order summary:\n{summary}\nTotal: ₹{total}\n\nWould you like to confirm this order? (yes/no)"
        else:
            return "None of the items matched our menu. Please try again with valid items."

    elif state == 'confirm_order':
        if 'yes' in user_input:
            session['state'] = 'wait_payment'
            return "Order confirmed! Preparing your order... Please wait for 10 seconds for payment instructions."
        else:
            session['state'] = 'show_menu'
            return "Okay, please re-enter your order."

    elif state == 'wait_payment':
        session['state'] = 'ask_payment'
        return "Please proceed to payment. Type 'yes' to continue."

    elif state == 'ask_payment':
        if 'yes' in user_input:
            session['state'] = 'paid'
            return "<form method='POST'><button type='submit' name='message' value='paid' style='padding:10px 20px;border:none;background-color:#28a745;color:white;border-radius:20px;'>Pay Now</button></form>"
        else:
            return "Let me know when you're ready to pay."

    elif state == 'paid':
        session['state'] = 'done'
        return f"Thank you, {user_info.get('name')}! Your food will be delivered in 10 minutes. Have a great day! 🍽️\n\nWould you like to place another order? (yes/no)"

    return "Sorry, I didn't understand that."

if __name__ == '__main__':
    app.run(debug=True)