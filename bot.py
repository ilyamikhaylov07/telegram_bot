import logging
from telegram import Update
from telegram.ext import CallbackContext, filters,  MessageHandler, CommandHandler, Updater

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

def handle_voice(update: Update, _: CallbackContext) -> None:
    voice = update.message.voice
    voice_file = voice.get_file()
    voice_file.download('voice_message.ogg')

    handle_voice_command('voice_message.ogg')
    update.message.reply_text("Я обработал ваш голосовой запрос")

def main() -> None:

    token = 'YOUR_BOT_TOKEN'

    updater = Updater(token, use_context=True)
    
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    dispatcher.add_handler(MessageHandler(filters.VOICE, handle_voice))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
