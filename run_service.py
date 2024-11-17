from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
from openai import OpenAI
client=OpenAI(api_key=""
# Function to handle start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. Send me any message and I will capture it.')

# Function to handle messages
def capture_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id
    print(f"Captured message: {user_message} from chat ID: {chat_id}")
    
    # Forward the captured message to the Rasa bot
    rasa_response = forward_to_rasa(chat_id, user_message)


    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
    {"role": "system", "content":f"You got answer from database on this question: {user_message}, make it more beuitful, because you are an assitant in wig shop. Don't start with hi or any other greetings, if in a request wasn't this. RETURN ONLY REVISED ANSWER. for greeting answer greeting as  assistant.If that's question about  address or phone, or any infro regarding salon please return it. Don't skip answer."},
    {"role": "user", "content": rasa_response}
  ]
)


    
    # Send the response back to the user
   # update.message.reply_text(rasa_response)
    update.message.reply_text(completion.choices[0].message.content)

# Function to forward message to Rasa bot
def forward_to_rasa(sender_id, message):
    rasa_url = "http://localhost:5005/webhooks/rest/webhook/"
    payload = {
        "sender": str(sender_id),
        "message": message
    }
    
    response = requests.post(
        rasa_url,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    if response.ok:
        rasa_messages = response.json()
        if rasa_messages:
            return rasa_messages[0].get('text', 'Sorry, I did not understand that.')
        else:
            return 'Sorry, I did not get a response from my server.'
    else:
        return 'Failed to connect to the server.'
    
def main():
    # Replace with your Telegram bot token
    token = '7335977975:AAEghYDIinBOEDwxTgzfiTo9XQDrsbVD4bI'
    
    # Set up the Updater
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the start command handler
    dp.add_handler(CommandHandler("start", start))

    # Register a handler for capturing messages
    # Register a handler for capturing messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, capture_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal (Ctrl+C)
    updater.idle()
main()

