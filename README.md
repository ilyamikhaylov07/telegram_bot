# 🤖 Telegram-бот Обойчик

Интерактивный Telegram-бот, который понимает сообщения пользователя с помощью модели машинного обучения и предлагает обои с кнопками прямо в чате. Отличный пример проекта с обработкой естественного языка и базовой рекомендательной системой.

---

## 🚀 Возможности

- 🧠 Определение намерений (intents) на основе текста пользователя  
- 💬 Ответы на фразы типа привет, как дела, пока  
- 🖼️ Показ товаров (обоев) с фото, описанием, ценой и кнопками  
- 🔁 Перелистывание карточек товаров  
- 📥 Обработка интерактивных кнопок (inline-клавиатура)  
- 🛠️ Гибкая настройка через JSON-файлы  

---

## 📂 Структура проекта

telegram_bot
├── bot.py # Основной код Telegram-бота
├── generate_intents.py # Генерация intents из диалогов
├── train_model.py # Обучение ML-модели
├── data
│ ├── dialogues.txt # Файл с вопросами, ответами и тегами
│ ├── intents.json # Сгенерированные intents
│ └── products.json # Товары (обои) с фото и описанием
├── model
│ ├── intent_model.pkl # Обученная модель логистической регрессии
│ └── vectorizer.pkl # TF-IDF векторизатор
└── README.md # Описание проекта

