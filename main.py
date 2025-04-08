import os
import requests
from bs4 import BeautifulSoup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import telebot
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_lang = {}

TEXT = {
    'ru': {
        'welcome': "Привет! Я бот поддержки резервистов и боевых раненых 🇮🇱",
        'language_selected': "Выбран язык: Русский",
        'reservist_loading': "⏳ Получаю информацию для резервистов...",
        'reservist_title': "🪖 Информация для резервистов:",
        'no_data': "Нет доступной информации.",
        'wounded': "🩼 Информация для боевых раненых будет добавлена в следующих версиях.",
        'choose_lang': "🌐 Выберите язык:",
    },
    'he': {
        'welcome': "שלום! אני בוט תמיכה לחיילי מילואים ונפגעי לחימה 🇮🇱",
        'language_selected': "השפה שנבחרה: עברית",
        'reservist_loading': "⏳ טוען מידע על מילואימניקים...",
        'reservist_title': "🪖 מידע למילואימניקים:",
        'no_data': "אין מידע זמין כעת.",
        'wounded': "🩼 מידע לנפגעי לחימה יתווסף בגרסאות הבאות.",
        'choose_lang': "🌐 בחר שפה:",
    }
}

def get_idf_news():
    try:
        url = 'https://www.idf.il/'
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='news-item')
        news_list = []
        for item in news_items[:3]:
            title = item.find('h3')
            link = item.find('a')
            if title and link:
                news_list.append(f"{title.text.strip()}\nСсылка: {link['href']}")
        return news_list
    except Exception as e:
        return [f"Ошибка: {e}"]

def get_gov_benefits():
    try:
        url = 'https://www.gov.il/he/Departments/General/benefits-for-reservists'
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        benefits = soup.find_all('li', class_='benefit-item')
        benefit_list = []
        for b in benefits[:3]:
            title = b.find('h4')
            desc = b.find('p')
            if title and desc:
                benefit_list.append(f"{title.text.strip()}\n{desc.text.strip()}")
        return benefit_list
    except Exception as e:
        return [f"Ошибка: {e}"]

def main_menu_keyboard(lang='ru'):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("🪖 Инфо для резервистов" if lang == 'ru' else "🪖 מידע למילואימניקים"),
        KeyboardButton("🩼 Инфо для раненых" if lang == 'ru' else "🩼 מידע לפצועים"),
    )
    kb.add(KeyboardButton("🌐 Сменить язык" if lang == 'ru' else "🌐 החלף שפה"))
    return kb

def language_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Русский"), KeyboardButton("עברית"))
    return kb

@bot.message_handler(commands=['start'])
def start(message):
    sticker_id = 'CAACAgIAAxkBAAEEZP1lX2kLrhb_lB_iECf3VnnhXJ6iTwACDQADVp29CnMl2W7JRY2NLwQ'  # Telegram sticker ID
    bot.send_sticker(message.chat.id, sticker_id)
    bot.send_message(message.chat.id, TEXT['ru']['choose_lang'], reply_markup=language_keyboard())

@bot.message_handler(func=lambda m: m.text in ["Русский", "עברית"])
def set_language(message):
    lang = 'ru' if message.text == "Русский" else 'he'
    user_lang[message.chat.id] = lang
    bot.send_message(message.chat.id, TEXT[lang]['language_selected'], reply_markup=main_menu_keyboard(lang))
    bot.send_message(message.chat.id, TEXT[lang]['welcome'])

@bot.message_handler(func=lambda m: m.text in ["🪖 Инфо для резервистов", "🪖 מידע למילואימניקים"])
def reservist_info(message):
    lang = user_lang.get(message.chat.id, 'ru')
    bot.send_message(message.chat.id, TEXT[lang]['reservist_loading'])

    news = get_idf_news()
    benefits = get_gov_benefits()

    bot.send_message(message.chat.id, TEXT[lang]['reservist_title'])

    if news:
        news_text = "\n\n".join(news).strip()
        if news_text:
            bot.send_message(message.chat.id, news_text)
        else:
            bot.send_message(message.chat.id, TEXT[lang]['no_data'])
    else:
        bot.send_message(message.chat.id, TEXT[lang]['no_data'])

    if benefits:
        benefits_text = "\n\n".join(benefits).strip()
        if benefits_text:
            bot.send_message(message.chat.id, benefits_text)
        else:
            bot.send_message(message.chat.id, TEXT[lang]['no_data'])
    else:
        bot.send_message(message.chat.id, TEXT[lang]['no_data'])

@bot.message_handler(func=lambda m: m.text in ["🩼 Инфо для раненых", "🩼 מידע לפצועים"])
def wounded_info(message):
    lang = user_lang.get(message.chat.id, 'ru')
    bot.send_message(message.chat.id, TEXT[lang]['wounded'])

@bot.message_handler(func=lambda m: m.text in ["🌐 Сменить язык", "🌐 החלף שפה"])
def change_language(message):
    bot.send_message(message.chat.id, TEXT['ru']['choose_lang'], reply_markup=language_keyboard())

# --- Запуск ---
if __name__ == '__main__':
    print("Бот запущен 🚀")
    bot.polling(none_stop=True)
