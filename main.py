import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or "ВАШ_ТОКЕН_ТУТ"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "ВАШ_GEMINI_API_KEY_ТУТ"

bot = telebot.TeleBot(BOT_TOKEN)

user_languages = {}
user_questions = []
faq_likes = {}

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

translations = {
    "choose_language": {"ru": "Выберите язык:", "en": "Choose a language:", "he": "בחר שפה:"},
    "main_menu": {"ru": "Выберите опцию:", "en": "Choose an option:", "he": "בחר אפשרות:"},
    "faq": {"ru": "❓ Часто задаваемые вопросы", "en": "❓ Frequently Asked Questions", "he": "❓ שאלות נפוצות"},
    "ask": {"ru": "✍ Задать свой вопрос", "en": "✍ Ask your question", "he": "✍ שאל שאלה"},
    "specialist": {"ru": "👨‍⚕️ Обратиться к специалисту", "en": "👨‍⚕️ Contact a specialist", "he": "👨‍⚕️ פנייה למומחה"},
    "spec_types": {"ru": "Выберите тип специалиста:", "en": "Choose specialist type:", "he": "בחר סוג מומחה:"},
    "psych": {"ru": "🧠 Психологическая помощь", "en": "🧠 Psychological Help", "he": "🧠 עזרה פסיכולוגית"},
    "finance": {"ru": "💰 Финансовая помощь", "en": "💰 Financial Help", "he": "💰 סיוע כלכלי"},
    "legal": {"ru": "⚖️ Юридическая помощь", "en": "⚖️ Legal Help", "he": "⚖️ עזרה משפטית"},
    "menu": {"ru": "🔙 В меню", "en": "🔙 Back to menu", "he": "🔙 חזרה לתפריט"},
    "change_lang": {"ru": "🌐 Сменить язык", "en": "🌐 Change language", "he": "🌐 שנה שפה"},
    "like_thanks": {"ru": "Спасибо за оценку!", "en": "Thanks for your feedback!", "he": "תודה על המשוב!"},
    "prompt_question": {"ru": "Введите ваш вопрос:", "en": "Please type your question:", "he": "כתוב את שאלתך:"},
    "error_ai": {"ru": "Произошла ошибка при получении ответа.", "en": "An error occurred while getting a response.", "he": "אירעה שגיאה בעת קבלת תשובה."},
    "no_more_questions": {"ru": "Это был последний вопрос. Возвращаем в меню.", "en": "That was the last question. Returning to the menu.", "he": "זו הייתה השאלה האחרונה. חוזרים לתפריט."}
}

base_faqs = [
    {
        "question": {
            "ru": "Какие льготы положены раненым солдатам?",
            "en": "What benefits are available for wounded soldiers?",
            "he": "אילו הטבות מגיעות לחיילים פצועים?"
        },
        "answer": {
            "ru": "Раненым солдатам положены медицинские, финансовые и социальные льготы.",
            "en": "Wounded soldiers are entitled to medical, financial, and social benefits.",
            "he": "לחיילים פצועים מגיעות הטבות רפואיות, כלכליות וחברתיות."
        }
    },
    {
        "question": {
            "ru": "Где получить помощь с реабилитацией?",
            "en": "Where can I get rehabilitation help?",
            "he": "היכן ניתן לקבל עזרה בשיקום?"
        },
        "answer": {
            "ru": "Обратитесь в ближайший реабилитационный центр или медицинское учреждение.",
            "en": "Contact the nearest rehabilitation center or medical facility.",
            "he": "פנה למרכז השיקום הקרוב או למוסד רפואי."
        }
    },
    {
        "question": {
            "ru": "Как подать заявление на пособие?",
            "en": "How to apply for benefits?",
            "he": "כיצד להגיש בקשה לקצבה?"
        },
        "answer": {
            "ru": "Вы можете подать заявление через портал государственных услуг или в МФЦ.",
            "en": "You can apply through the public services portal or a service center.",
            "he": "ניתן להגיש בקשה דרך פורטל השירותים הציבוריים או במרכז שירות."
        }
    },
    {
        "question": {
            "ru": "Какие документы нужны для получения льгот?",
            "en": "What documents are needed to receive benefits?",
            "he": "אילו מסמכים נדרשים לקבלת הטבות?"
        },
        "answer": {
            "ru": "Паспорт, медицинское заключение, удостоверение участника боевых действий.",
            "en": "Passport, medical report, and combatant ID are required.",
            "he": "נדרש דרכון, חוות דעת רפואית ותעודת לוחם."
        }
    },
    {
        "question": {
            "ru": "Можно ли получить психологическую помощь?",
            "en": "Can I get psychological help?",
            "he": "האם ניתן לקבל עזרה נפשית?"
        },
        "answer": {
            "ru": "Да, вы можете обратиться к военному психологу или в центр поддержки ветеранов.",
            "en": "Yes, you can contact a military psychologist or a veteran support center.",
            "he": "כן, ניתן לפנות לפסיכולוג צבאי או למרכז תמיכה לוותיקים."
        }
    },
    {
        "question": {
            "ru": "Как долго длится процесс восстановления?",
            "en": "How long does the recovery process take?",
            "he": "כמה זמן נמשך תהליך השיקום?"
        },
        "answer": {
            "ru": "Это индивидуально, зависит от степени травмы и типа лечения.",
            "en": "It depends on the injury and type of treatment. Each case is different.",
            "he": "זה תלוי בפציעה ובסוג הטיפול. כל מקרה שונה."
        }
    },
    {
        "question": {
            "ru": "Есть ли льготы для членов семьи?",
            "en": "Are there benefits for family members?",
            "he": "האם יש הטבות לבני משפחה?"
        },
        "answer": {
            "ru": "Да, для членов семьи также предусмотрены определённые социальные льготы.",
            "en": "Yes, there are also specific social benefits for family members.",
            "he": "כן, יש גם הטבות חברתיות מסוימות לבני משפחה."
        }
    },
    {
        "question": {
            "ru": "Кто может помочь с юридическими вопросами?",
            "en": "Who can help with legal issues?",
            "he": "מי יכול לעזור בנושאים משפטיים?"
        },
        "answer": {
            "ru": "Юридическую помощь можно получить в государственных центрах или НКО.",
            "en": "Legal aid is available at government centers or NGOs.",
            "he": "ניתן לקבל סיוע משפטי במרכזים ממשלתיים או בעמותות."
        }
    },
    {
        "question": {
            "ru": "Как получить компенсацию за потерю трудоспособности?",
            "en": "How to get compensation for disability?",
            "he": "כיצד ניתן לקבל פיצוי על אובדן כושר עבודה?"
        },
        "answer": {
            "ru": "Нужно пройти медицинскую комиссию и подать документы в ФСС.",
            "en": "You must pass a medical evaluation and submit documents to the social insurance.",
            "he": "יש לעבור ועדה רפואית ולהגיש מסמכים לביטוח הלאומי."
        }
    },
    {
        "question": {
            "ru": "Где найти сообщество таких же пострадавших?",
            "en": "Where can I find a community of others affected?",
            "he": "היכן ניתן למצוא קהילה של נפגעים נוספים?"
        },
        "answer": {
            "ru": "Существуют цифровые платформы поддержки и группы в соцсетях.",
            "en": "There are digital support platforms and social media groups.",
            "he": "ישנן פלטפורמות תמיכה דיגיטליות וקבוצות ברשתות החברתיות."
        }
    }
]

@bot.message_handler(commands=['start'])
def start(message):
    show_language_menu(message.chat.id)

def show_language_menu(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("\ud83c\uddf7\ud83c\uddfa Русский", callback_data="lang_ru"),
        InlineKeyboardButton("\ud83c\uddfa\ud83c\uddf8 English", callback_data="lang_en"),
        InlineKeyboardButton("\ud83c\uddee\ud83c\uddf1 \u05e2\u05d1\u05e8\u05d9\u05ea", callback_data="lang_he")
    )
    bot.send_message(chat_id, "Choose language / Выберите язык / בחר שפה:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def set_language(call):
    lang = call.data.split("_")[1]
    user_languages[call.from_user.id] = lang
    show_main_menu(call.message.chat.id, lang)

def show_main_menu(chat_id, lang):
    text = translations["main_menu"][lang]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(translations["faq"][lang], callback_data="faq"),
        InlineKeyboardButton(translations["ask"][lang], callback_data="ask"),
        InlineKeyboardButton(translations["specialist"][lang], callback_data="specialist"),
        InlineKeyboardButton(translations["change_lang"][lang], callback_data="change_lang")
    )
    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "change_lang")
def change_lang(call):
    show_language_menu(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "faq")
def show_faq(call):
    lang = user_languages.get(call.from_user.id, "ru")
    send_faq_page(call.message.chat.id, 0, lang)

def send_faq_page(chat_id, page, lang):
    faqs = base_faqs + user_questions
    if page >= len(base_faqs):
        bot.send_message(chat_id, translations["no_more_questions"][lang])
        show_main_menu(chat_id, lang)
        return
    faq = faqs[page]
    q = faq["question"].get(lang, faq["question"].get("ru", ""))
    a = faq["answer"].get(lang, faq["answer"].get("ru", ""))
    text = f"Q: {q}\nA: {a}"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("\ud83d\udc4d", callback_data=f"like_{page}"))
    if page + 1 < len(base_faqs):
        keyboard.add(InlineKeyboardButton("\u27a1\ufe0f", callback_data=f"faq_page:{page+1}"))
    keyboard.add(InlineKeyboardButton(translations["menu"][lang], callback_data="menu"))

    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("faq_page:"))
def paginate_faq(call):
    page = int(call.data.split(":")[1])
    lang = user_languages.get(call.from_user.id, "ru")
    send_faq_page(call.message.chat.id, page, lang)

@bot.callback_query_handler(func=lambda call: call.data.startswith("like_"))
def like_faq(call):
    index = int(call.data.split("_")[1])
    faq_likes[index] = faq_likes.get(index, 0) + 1
    lang = user_languages.get(call.from_user.id, "ru")
    bot.answer_callback_query(call.id, translations["like_thanks"][lang])

@bot.callback_query_handler(func=lambda call: call.data == "ask")
def ask_question(call):
    lang = user_languages.get(call.from_user.id, "ru")
    msg = bot.send_message(call.message.chat.id, translations["prompt_question"][lang])
    bot.register_next_step_handler(msg, receive_question)

def receive_question(msg):
    question = msg.text
    lang = user_languages.get(msg.from_user.id, "ru")
    try:
        response = model.generate_content(question)
        answer = response.text.strip()
    except Exception:
        answer = translations["error_ai"][lang]

    user_questions.append({"question": {lang: question}, "answer": {lang: answer}})
    bot.send_message(msg.chat.id, answer)
    show_main_menu(msg.chat.id, lang)

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def back_to_menu(call):
    lang = user_languages.get(call.from_user.id, "ru")
    show_main_menu(call.message.chat.id, lang)

@bot.callback_query_handler(func=lambda call: call.data == "specialist")
def specialist_menu(call):
    lang = user_languages.get(call.from_user.id, "ru")
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(translations["psych"][lang], callback_data="spec_psych"),
        InlineKeyboardButton(translations["finance"][lang], callback_data="spec_finance"),
        InlineKeyboardButton(translations["legal"][lang], callback_data="spec_legal")
    )
    keyboard.add(InlineKeyboardButton(translations["menu"][lang], callback_data="menu"))
    bot.send_message(call.message.chat.id, translations["spec_types"][lang], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("spec_"))
def show_specialist_info(call):
    lang = user_languages.get(call.from_user.id, "ru")
    key = call.data
    content = {
        "spec_psych": {
            "ru": "🧠 Психологическая помощь\n\nНужна поддержка? Вот полезные ресурсы:",
            "en": "🧠 Psychological Help\n\nNeed support? Here are helpful resources:",
            "he": "🧠 עזרה פסיכולוגית\n\nזקוקים לתמיכה? הנה מקורות עזר:"
        },
        "spec_finance": {
            "ru": "💰 Финансовая помощь\n\nДотации и поддержка от государства:",
            "en": "💰 Financial Help\n\nGovernment grants and support:",
            "he": "💰 סיוע כלכלי\n\nמענקים ותמיכה מהמדינה:"
        },
        "spec_legal": {
            "ru": "⚖️ Юридическая помощь\n\nБесплатные юридические консультации:",
            "en": "⚖️ Legal Help\n\nFree legal consultations:",
            "he": "⚖️ עזרה משפטית\n\nייעוץ משפטי חינם:"
        }
    }

    links = {
        "spec_psych": "https://www.kolzchut.org.il",
        "spec_finance": "https://www.btl.gov.il",
        "spec_legal": "https://www.kolzchut.org.il"
    }

    msg = content[key][lang]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔗 Перейти на сайт", url=links[key]))
    keyboard.add(InlineKeyboardButton(translations["menu"][lang], callback_data="menu"))
    bot.send_message(call.message.chat.id, msg, reply_markup=keyboard)

bot.polling(none_stop=True)
