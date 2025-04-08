import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or "ВАШ_ТОКЕН_ТУТ"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "ВАШ_GEMINI_API_KEY_ТУТ"

bot = telebot.TeleBot(BOT_TOKEN)

FAQ_FILE = "user_faqs.json"
user_languages = {}

# Инициализация Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

base_faqs = [
    {"question": "Какие льготы положены раненым солдатам?", "answer": "Раненым солдатам положены медицинские, финансовые и социальные льготы."},
    {"question": "Где получить помощь с реабилитацией?", "answer": "Обратитесь в ближайший реабилитационный центр или медицинское учреждение."},
    {"question": "Как подать заявление на пособие?", "answer": "Вы можете подать заявление через портал государственных услуг или в МФЦ."},
    {"question": "Какие документы нужны для получения льгот?", "answer": "Паспорт, медицинское заключение, удостоверение участника боевых действий."},
    {"question": "Можно ли получить психологическую помощь?", "answer": "Да, вы можете обратиться к военному психологу или в центр поддержки ветеранов."},
    {"question": "Как долго длится процесс восстановления?", "answer": "Это индивидуально, зависит от степени травмы и типа лечения."},
    {"question": "Есть ли льготы для членов семьи?", "answer": "Да, для членов семьи также предусмотрены определённые социальные льготы."},
    {"question": "Кто может помочь с юридическими вопросами?", "answer": "Юридическую помощь можно получить в государственных центрах или НКО."},
    {"question": "Как получить компенсацию за потерю трудоспособности?", "answer": "Нужно пройти медицинскую комиссию и подать документы в ФСС."},
    {"question": "Где найти сообщество таких же пострадавших?", "answer": "Существуют цифровые платформы поддержки и группы в соцсетях."}
]

user_questions = []
faq_likes = {}

@bot.message_handler(commands=['start'])
def start(message):
    lang_keyboard = InlineKeyboardMarkup()
    lang_keyboard.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇮🇱 עברית", callback_data="lang_he"),
        InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
    )
    bot.send_message(message.chat.id, "Выберите язык / בחר שפה / Choose language:", reply_markup=lang_keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def set_language(call):
    lang = call.data.split("_")[1]
    user_languages[call.from_user.id] = lang
    show_main_menu(call.message.chat.id, lang)

def show_main_menu(chat_id, lang, edit=False, message_id=None):
    texts = {
        "ru": "Выберите опцию:",
        "he": "בחר אפשרות:",
        "en": "Choose an option:"
    }
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("❓ Часто задаваемые вопросы", callback_data="faq"))
    keyboard.add(InlineKeyboardButton("✍ Задать свой вопрос", callback_data="ask"))
    if edit:
        bot.edit_message_text(texts[lang], chat_id, message_id, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, texts[lang], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "faq")
def show_faq(call):
    send_faq_page(call.message.chat.id, 0, user_languages.get(call.from_user.id, "ru"))

def send_faq_page(chat_id, page, lang):
    faqs = base_faqs + user_questions
    if page >= len(faqs):
        bot.send_message(chat_id, "Больше нет вопросов." if lang == "ru" else "No more questions.")
        return
    faq = faqs[page]
    text = f"Q: {faq['question']}\nA: {faq['answer']}"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("👍 Мне помогло", callback_data=f"like_{page}"))
    if page + 1 < len(faqs):
        keyboard.add(InlineKeyboardButton("➡️ Далее", callback_data=f"faq_page:{page+1}"))
    keyboard.add(InlineKeyboardButton("🔙 В меню", callback_data="menu"))
    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("faq_page:"))
def paginate_faq(call):
    page = int(call.data.split(":")[1])
    send_faq_page(call.message.chat.id, page, user_languages.get(call.from_user.id, "ru"))

@bot.callback_query_handler(func=lambda call: call.data.startswith("like_"))
def like_faq(call):
    index = int(call.data.split("_")[1])
    faq_likes[index] = faq_likes.get(index, 0) + 1
    bot.answer_callback_query(call.id, "Спасибо за оценку!")

@bot.callback_query_handler(func=lambda call: call.data == "ask")
def ask_question(call):
    lang = user_languages.get(call.from_user.id, "ru")
    prompt = {"ru": "Введите ваш вопрос:", "he": "כתוב את שאלתך:", "en": "Please type your question:"}[lang]
    msg = bot.send_message(call.message.chat.id, prompt)
    bot.register_next_step_handler(msg, receive_question)

def receive_question(msg):
    question = msg.text
    lang = user_languages.get(msg.from_user.id, "ru")
    try:
        response = model.generate_content(question)
        ai_answer = response.text.strip()
    except Exception as e:
        ai_answer = {
            "ru": "Произошла ошибка при получении ответа.",
            "he": "אירעה שגיאה בעת קבלת תשובה.",
            "en": "An error occurred while getting a response."
        }[lang]
    user_questions.append({"question": question, "answer": ai_answer})
    bot.send_message(msg.chat.id, f"{ai_answer}")
    show_main_menu(msg.chat.id, lang)

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def back_to_menu(call):
    lang = user_languages.get(call.from_user.id, "ru")
    show_main_menu(call.message.chat.id, lang, edit=True, message_id=call.message.message_id)

bot.polling(none_stop=True)
