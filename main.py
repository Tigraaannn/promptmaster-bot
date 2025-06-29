from telebot import TeleBot, types
import os

# Используй свой токен или переменную окружения
BOT_TOKEN = os.getenv("7745018927:AAFwuF_mRCz1o-iJKcgRFGv9EhVFFuXCPIE")  # Либо вставь прямо: '123456:ABC...'

bot = TeleBot('7745018927:AAFwuF_mRCz1o-iJKcgRFGv9EhVFFuXCPIE')

# === Главное меню ===
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row("📚 Учёба", "💼 Бизнес")
main_menu.row("🖼️ Картинки", "🎬 Видео")

# === Подменю "Учёба" ===
study_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
study_menu.row("📄 Реферат", "📄 Конспект лекции")
study_menu.row("🔙 Назад")

# === Подменю "Бизнес" ===
business_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
business_menu.row("💬 Оффер", "📃 Лендинг")
business_menu.row("✉️ Деловое письмо", "📸 Пост в Instagram")
business_menu.row("🔙 Назад")

# === Стартовое сообщение ===
@bot.message_handler(commands=["start"])
def send_welcome(message):
    text = (
        "🤖 Привет! Я — ПромтМастер.\n\n"
        "Я бот, который помогает тебе работать с ИИ быстрее и лучше. "
        "Здесь ты найдёшь готовые промты для ChatGPT, Midjourney, Pika и других инструментов.\n\n"
        "🔹 Учёба и бизнес\n"
        "🔹 Генерация изображений и видео\n"
        "🔹 Кастомные промты под твой запрос\n\n"
        "Выбери категорию ниже, чтобы начать:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu)

# === Обработка нажатий на категории ===
@bot.message_handler(func=lambda msg: msg.text in ["📚 Учёба", "💼 Бизнес", "🖼️ Картинки", "🎬 Видео"])
def handle_category(message):
    if message.text == "📚 Учёба":
        bot.send_message(message.chat.id, "Выбери промт:", reply_markup=study_menu)
    elif message.text == "💼 Бизнес":
        bot.send_message(message.chat.id, "Выбери промт:", reply_markup=business_menu)
    elif message.text == "🖼️ Картинки":
        send_docx(message.chat.id, "image_generation_prompt_template.docx")
    elif message.text == "🎬 Видео":
        send_docx(message.chat.id, "video_prompt_template.docx")

# === Промты для учебы ===
@bot.message_handler(func=lambda msg: msg.text in ["📄 Реферат", "📄 Конспект лекции"])
def handle_study(message):
    files = {
        "📄 Реферат": "ref_prompt_template.docx",
        "📄 Конспект лекции": "lecture_summary_prompt_template.docx"
    }
    send_docx(message.chat.id, files[message.text])

# === Промты для бизнеса ===
@bot.message_handler(func=lambda msg: msg.text in ["💬 Оффер", "📃 Лендинг", "✉️ Деловое письмо", "📸 Пост в Instagram"])
def handle_business(message):
    files = {
        "💬 Оффер": "offer_prompt_template.docx",
        "📃 Лендинг": "landing_prompt_template.docx",
        "✉️ Деловое письмо": "business_letter_prompt_template.docx",
        "📸 Пост в Instagram": "instagram_post_prompt_template.docx"
    }
    send_docx(message.chat.id, files[message.text])

# === Назад ===
@bot.message_handler(func=lambda msg: msg.text == "🔙 Назад")
def back_to_main(message):
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu)

# === Отправка файла .docx ===
def send_docx(chat_id, filename):
    path = os.path.join(os.getcwd(), filename)
    if os.path.exists(path):
        with open(path, "rb") as doc:
            bot.send_document(chat_id, doc)
    else:
        bot.send_message(chat_id, f"⚠️ Файл не найден: {filename}")

# === Запуск ===
if __name__ == "__main__":
    print("Бот запущен.")
    bot.infinity_polling()
