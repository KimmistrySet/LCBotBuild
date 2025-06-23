from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interactions,db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Interaction model
class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(256), nullable=False)
    bot_response= db.Column(db.String(256), nullable=False)

# Create the database and the table
with app.app_context():
    db.create_all()

# In-memory store for user states (for demonstration purposes)
user_states = {}

# A simple rule-based response system
def get_bot_response(user_input, user_id):
    if user_id not in user_states:
        # Prompt for username if not set
        user_states[user_id] = {'username' : None}
        return "Hello! What's your name?"
    
    # If username is not provided, ask for it
    if user_states [user_id]['username'] is None:
        user_states[user_id]['username'] = user_input
        return f"Nice to meet you, {user_input}! How can I assist you today?"
    
    #Otherwise, handle regular queries
    user_input = user_input.lower()
    if "order" in user_input:
        return "You can check your order status on our website under 'Order Tracking'."
    elif "support" in user_input:
        return "For support, please visit our Help Center or contact support@example.com."
    elif "thank you" in user_input:
        return "You're welcome! If you have any more questions, feel free to ask."
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase your request?"
    
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message', '')
    user_id = data.get('user_id' 'default_user')

    bot_response = get_bot_response(user_message, user_id)

    # Store interaction in the database
    interaction = Interaction(user_message=user_message, bot_response=bot_response)
    db.session.add(interaction)
    db.session.commit()

    return jsonify({'response' : bot_response})

if _name_ == "_main_":
    app.run(debug=True)

