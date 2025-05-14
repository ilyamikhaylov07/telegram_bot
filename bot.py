import telebot
import json
import pickle
from random import choice
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Инициализация бота
bot = telebot.TeleBot("apitelegram")  

# Загрузка модели и данных
with open('model/intent_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('data/intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Предсказание намерения
def get_intent(text):
    vec = vectorizer.transform([text])
    tag = model.predict(vec)[0]
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return choice(intent['responses']), tag
    return "Извините, я не понял ваш запрос.", None

# Отправка одного товара с кнопками
product_index = {}

def send_product_with_buttons(chat_id, user_id):
    index = product_index.get(user_id, 0)
    if index >= len(products):
        bot.send_message(chat_id, "Больше товаров нет. Напишите, если нужно что-то ещё!")
        return

    product = products[index]
    caption = f"\U0001F4CC {product['name']}\n\U0001F4DD {product['desc']}\n\U0001F4B0 {product['price']}"
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Следующий", callback_data="next_product"),
        InlineKeyboardButton("Стоп", callback_data="stop_products")
    )
    bot.send_photo(chat_id, product['image_url'], caption=caption, reply_markup=markup)
    product_index[user_id] = index + 1

# Показ кнопок перехода к товарам
def show_inline_buttons(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Да, покажи обои", callback_data="show_wallpapers"),
        InlineKeyboardButton("Нет, спасибо", callback_data="no_thanks")
    )
    bot.send_message(chat_id, "Интересуетесь обновлением интерьера?", reply_markup=markup)

# Команда /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! Я Обойчик 😇 😃!!!. Просто напишите, что вас интересует.")

# Обработка обычных сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.strip()
    response, tag = get_intent(user_text)

    print(f"[DEBUG] Получено сообщение: {user_text} | Предсказанный тег: {tag}")

    if tag is None:
        bot.send_message(message.chat.id, response)
        return

    if tag.startswith("smalltalk_"):
        bot.send_message(message.chat.id, response)
        if tag in ["smalltalk_home", "ad_wallpaper_redirect"]:
            show_inline_buttons(message.chat.id)

    elif tag == "ad_wallpaper_offer":
        bot.send_message(message.chat.id, response)
        bot.send_message(message.chat.id, "Вот некоторые варианты, которые могут вам понравиться:")
        product_index[message.chat.id] = 0
        send_product_with_buttons(message.chat.id, message.chat.id)

    else:
        bot.send_message(message.chat.id, response)

# Обработка callback-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "show_wallpapers":
        bot.send_message(call.message.chat.id, "Супер! Вот подборка популярных обоев:")
        product_index[call.message.chat.id] = 0
        send_product_with_buttons(call.message.chat.id, call.message.chat.id)

    elif call.data == "no_thanks":
        bot.send_message(call.message.chat.id, "Хорошо, если передумаете — просто напишите!")

    elif call.data == "next_product":
        send_product_with_buttons(call.message.chat.id, call.message.chat.id)

    elif call.data == "stop_products":
        bot.send_message(call.message.chat.id, "Если захотите вернуться к выбору — напишите мне!")

# Запуск бота
print("Бот запущен...")
bot.polling(none_stop=True)