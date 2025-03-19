import logging
from telegram import Update
from telegram.ext import CallbackContext

logging.basicConfig(format='%(ascitime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Привет! Чем могу помочь?')

def handle_text(update: Update, _: CallbackContext) -> None:
    user_message = update.message.text.lower()
    #TODO сделать метод для намерений и в целом класс
    intent = classify_intent(user_message)

    if intent == 'products':
        products = get_product_recommendations()
        update.message.reply_text(f"Рекомендуемые товары: {', '.join(products)}")
    elif intent == 'greeting':
        update.message.reply_text("Привет! Чем могу помочь?")
    else:
        user_message, bot_message = get_random_dialogue()
        update.message.reply_text(bot_message) 

    
