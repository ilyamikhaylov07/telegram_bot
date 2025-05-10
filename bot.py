import telebot
import json
import pickle
from random import choice


bot = telebot.TeleBot("token")

# Загрузка модели и векторизатора
with open('model/intent_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('data/intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Функция предсказания
def get_intent(text):
    vec = vectorizer.transform([text])
    tag = model.predict(vec)[0]
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return choice(intent['responses']), tag
    return "Извините, я не понял ваш запрос.", None


print("Бот запущен...")
bot.polling()
