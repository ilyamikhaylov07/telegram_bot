import telebot
from random import choice
from bot import bot, get_intent, products

# Обработчики сообщений
@bot.message_handler(commands=['start'])
def handle_start(message):
    text = (
        "Привет! 👋 Я бот-помощник по выбору обоев.\n"
        "Ты можешь спросить меня о разных вещах, а я подскажу.\n"
        "Например, напиши: 'Хочу купить обои'."
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    response, tag = get_intent(message.text)

    # Если это запрос на покупку обоев
    if tag in ["intent_14", "intent_15", "intent_16", "intent_17", "intent_18", "intent_19", "intent_20", "intent_21", "intent_22", "intent_23"]:
        bot.send_message(message.chat.id, response)
        for prod in products:
            bot.send_message(
                message.chat.id,
                f"📌 {prod['name']}\n📝 {prod['desc']}\n💰 {prod['price']}"
            )
            if 'image_url' in prod:  # Если есть ссылка на изображение
                bot.send_photo(message.chat.id, prod['image_url'])

    # Если это не запрос на товары
    else:
        bot.send_message(message.chat.id, response)