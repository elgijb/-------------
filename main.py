import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import json
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

FAQ_FILE = "user_faqs.json"

user_languages = {}

base_faqs_ru = [
    {"question": "Как оформить статус раненого?", "answer": "Необходимо обратиться в военкомат с медицинскими документами.", "likes": 0},
    {"question": "Какие выплаты положены после ранения?", "answer": "Компенсации зависят от степени повреждения. Обратитесь в соцзащиту.", "likes": 0},
    {"question": "Где пройти реабилитацию?", "answer": "Вам должны предложить центр реабилитации по месту жительства.", "likes": 0},
    {"question": "Как получить психологическую помощь?", "answer": "Позвоните на горячую линию Минобороны или обратитесь в клинику.", "likes": 0},
    {"question": "Как восстановить документы после ранения?", "answer": "Обратитесь в МФЦ с удостоверением личности и справкой.", "likes": 0},
    {"question": "Положена ли инвалидность?", "answer": "Это определяется медкомиссией по итогам обследования.", "likes": 0},
    {"question": "Что делать при потере трудоспособности?", "answer": "Можно оформить пособие по временной нетрудоспособности.", "likes": 0},
    {"question": "Где найти юриста для консультации?", "answer": "Воспользуйтесь бесплатной юрпомощью в регионе.", "likes": 0},
    {"question": "Как перевестись на другую службу после ранения?", "answer": "Обратитесь к командиру части или в кадровый отдел.", "likes": 0},
    {"question": "Что делать, если не выплачивают компенсацию?", "answer": "Подайте жалобу в военную прокуратуру или в суд.", "likes": 0},
]

base_faqs_he = [
    {"question": "איך מקבלים מעמד של פצוע קרב?", "answer": "צריך לפנות ללשכת הגיוס עם מסמכים רפואיים.", "likes": 0},
    {"question": "אילו תשלומים מגיעים אחרי פציעה?", "answer": "פיצויים תלויים בדרגת הפציעה. יש לפנות לרווחה.", "likes": 0},
    {"question": "איפה אפשר לעבור שיקום?", "answer": "צריך לקבל מרכז שיקום לפי מקום מגורים.", "likes": 0},
    {"question": "איך לקבל עזרה פסיכולוגית?", "answer": "פנה לקו חם של משרד הביטחון או לקליניקה.", "likes": 0},
    {"question": "איך לשחזר מסמכים אחרי פציעה?", "answer": "פנה למרכז שירות עם תעודה מזהה ואישור רפואי.", "likes": 0},
    {"question": "האם מגיעה נכות?", "answer": "זה נקבע על ידי ועדה רפואית לאחר בדיקה.", "likes": 0},
    {"question": "מה לעשות אם לא יכול לעבוד?", "answer": "ניתן להגיש בקשה לקצבת אי כושר זמנית.", "likes": 0},
    {"question": "איפה למצוא ייעוץ משפטי?", "answer": "יש לפנות לסיוע משפטי חינם באזורך.", "likes": 0},
    {"question": "איך לעבור תפקיד בצבא לאחר פציעה?", "answer": "פנה למפקד היחידה או למחלקת כוח אדם.", "likes": 0},
    {"question": "מה לעשות אם לא משלמים פיצוי?", "answer": "הגש תלונה לפרקליטות הצבאית או לבית המשפט.", "likes": 0},
]

def load_user_faqs():
    try:
        with open(FAQ_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_user_faqs(faqs):
    with open(FAQ_FILE, 'w', encoding='utf-8') as f:
        json.dump(faqs, f, ensure_ascii=False, indent=2)

@bot.message_handler(commands=['start'])
def choose_language(msg):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Русский", callback_data="lang:ru"))
    keyboard.add(InlineKeyboardButton("עברית", callback_data="lang:he"))
    bot.send_message(msg.chat.id, "Выберите язык / בחר שפה:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang:"))
def set_language(call):
    lang = call.data.split(":")[1]
    user_languages[call.from_user.id] = lang
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Часто задаваемые вопросы" if lang == "ru" else "שאלות נפוצות", callback_data="faq_page:0"))
    keyboard.add(InlineKeyboardButton("Задать свой вопрос" if lang == "ru" else "שאל שאלה", callback_data="ask"))
    welcome = "Добро пожаловать! Выберите действие:" if lang == "ru" else "ברוך הבא! בחר פעולה:"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=welcome, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("faq_page"))
def paginate_faq(call: CallbackQuery):
    lang = user_languages.get(call.from_user.id, "ru")
    page = int(call.data.split(":")[1])
    user_faqs = load_user_faqs()
    all_faqs = (base_faqs_ru if lang == "ru" else base_faqs_he) + user_faqs

    if page >= len(all_faqs): page = 0
    faq = all_faqs[page]

    keyboard = InlineKeyboardMarkup()
    if page > 0:
        keyboard.add(InlineKeyboardButton("← Назад" if lang == "ru" else "← חזור", callback_data=f"faq_page:{page - 1}"))
    if page < len(all_faqs) - 1:
        keyboard.add(InlineKeyboardButton("Вперёд →" if lang == "ru" else "→ הבא", callback_data=f"faq_page:{page + 1}"))
    keyboard.add(InlineKeyboardButton(("👍 Мне помогло" if lang == "ru" else "👍 זה עזר לי") + f" ({faq.get('likes', 0)})", callback_data=f"like:{page}"))

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f"Вопрос: {faq['question']}\nОтвет: {faq['answer']}" if lang == "ru" else f"שאלה: {faq['question']}\nתשובה: {faq['answer']}",
                          reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("like:"))
def like_faq(call: CallbackQuery):
    page = int(call.data.split(":")[1])
    user_faqs = load_user_faqs()
    lang = user_languages.get(call.from_user.id, "ru")

    if page < 10:
        (base_faqs_ru if lang == "ru" else base_faqs_he)[page]['likes'] += 1
    else:
        idx = page - 10
        user_faqs[idx]['likes'] += 1
        save_user_faqs(user_faqs)

    paginate_faq(CallbackQuery(id=call.id, from_user=call.from_user, message=call.message, data=f"faq_page:{page}"))
    bot.answer_callback_query(call.id, "Спасибо!" if lang == "ru" else "תודה!")

@bot.callback_query_handler(func=lambda call: call.data.startswith("like:"))
def like_faq(call: CallbackQuery):
    page = int(call.data.split(":")[1])
    user_faqs = load_user_faqs()
    lang = user_languages.get(call.from_user.id, "ru")

    if page < 10:
        (base_faqs_ru if lang == "ru" else base_faqs_he)[page]['likes'] += 1
    else:
        idx = page - 10
        user_faqs[idx]['likes'] += 1
        save_user_faqs(user_faqs)

    call.data = f"faq_page:{page}"
    paginate_faq(call)
    bot.answer_callback_query(call.id, "Спасибо!" if lang == "ru" else "תודה!")


def receive_question(msg):
    question = msg.text
    sent = bot.send_message(msg.chat.id, "Введите ответ на вопрос (или '-' если не знаете):" if user_languages.get(msg.from_user.id, "ru") == "ru" else "כתוב תשובה או '-' אם אינך יודע:")
    bot.register_next_step_handler(sent, lambda m: store_faq(m, question))

def store_faq(msg, question):
    answer = msg.text if msg.text != "-" else ""
    user_faqs = load_user_faqs()
    user_faqs.append({"question": question, "answer": answer, "likes": 0})
    save_user_faqs(user_faqs)
    bot.send_message(msg.chat.id, "Спасибо! Ваш вопрос добавлен." if user_languages.get(msg.from_user.id, "ru") == "ru" else "תודה! השאלה שלך נוספה.")

bot.polling(none_stop=True)
