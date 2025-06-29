import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# 🔒 Храним, кто вводит кастомный промт
user_states = {}

# 📁 Названия файлов
PROMPT_FILES = {
    "Учёба": {
        "Реферат": "ref_prompt_template.docx",
        "Конспект лекции": "lecture_summary_prompt_template.docx"
    },
    "Бизнес": {
        "Оффер": "offer_prompt_template.docx",
        "Лендинг": "landing_prompt_template.docx",
        "Деловое письмо": "business_letter_prompt_template.docx",
        "Instagram пост": "instagram_post_prompt_template.docx"
    },
    "Генерация изображений": {
        "Промт для картинки": "image_generation_prompt_template.docx"
    },
    "Генерация видео": {
        "Промт для видео": "video_prompt_template.docx"
    }
}

# ✨ Приветствие
WELCOME_TEXT = """
👋 Привет! Я — бот PromptMaster.

Я помогу тебе получить профессиональные промты для искусственного интеллекта — для учёбы, бизнеса, генерации изображений и видео.

📌 Просто выбери категорию — и я пришлю нужные шаблоны.

Хочешь что-то своё? Жми ✍️ Кастомный промт.
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in PROMPT_FILES.keys():
        markup.add(category)
    markup.add("✍️ Кастомный промт")
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in PROMPT_FILES)
def show_prompts(msg):
    category = msg.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for title in PROMPT_FILES[category]:
        markup.add(title)
    markup.add("⬅️ Назад")
    bot.send_message(msg.chat.id, f"📂 {category}: выбери промт", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "⬅️ Назад")
def back(msg):
    send_welcome(msg)

@bot.message_handler(func=lambda msg: msg.text == "✍️ Кастомный промт")
def custom_prompt_start(msg):
    user_states[msg.chat.id] = "awaiting_custom"
    bot.send_message(msg.chat.id, "✏️ Напиши, какой промт тебе нужен — я передам его команде!")

@bot.message_handler(func=lambda msg: user_states.get(msg.chat.id) == "awaiting_custom")
def handle_custom_prompt(msg):
    bot.send_message(msg.chat.id, "✅ Спасибо! Мы получили твой кастомный запрос.")
    user_states.pop(msg.chat.id)

@bot.message_handler(func=lambda msg: True)
def send_file(msg):
    for prompts in PROMPT_FILES.values():
        if msg.text in prompts:
            try:
                with open(prompts[msg.text], "rb") as f:
                    bot.send_document(msg.chat.id, f)
            except:
                bot.send_message(msg.chat.id, "❗Файл не найден.")
            return
    bot.send_message(msg.chat.id, "Я не понял. Пожалуйста, выбери вариант с кнопки.")

bot.polling(none_stop=True)
