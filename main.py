import os
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Временное хранилище выбора языка
user_lang = {}

# --- Тексты на двух языках ---
TEXT = {
    'ru': {
        'welcome': "Привет! Я бот поддержки резервистов и боевых раненых.\n\nВыберите язык:",
        'help': "/start - Начать\n/help - Помощь\n/reservist - Инфо для резервистов\n/wounded - Инфо для раненых",
        'language_selected': "Выбран язык: Русский",
        'reservist_loading': "Получаю информацию для резервистов...",
        'reservist_title': "Информация для резервистов:",
        'wounded': "Информация для боевых раненых будет добавлена в следующих версиях.",
    },
    'he': {
        'welcome': "שלום! אני בוט תמיכה לחיילי מילואים ונפגעי לחימה.\n\nבחר שפה:",
        'help': "/start - התחלה\n/help - עזרה\n/reservist - מידע למילואימניקים\n/wounded - מידע לפצועים",
        'language_selected': "השפה שנבחרה: עברית",
        'reservist_loading': "טוען מידע על מילואימניקים...",
        'reservist_title': "מידע למילואימניקים:",
        'wounded': "מידע לנפגעי לחימה יתווסף בגרסאות הבאות.",
    }
}

# --- Парсеры ---

def get_idf_news():
    try:
        url = 'https://www.idf.il/אתר-צה"ל/חדשות'
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='news-item')
        return [f"{item.find('h3').text.strip()}\nСсылка: {item.find('a')['href']}" for item in news_items[:3]]
    except Exception as e:
        return [f"Ошибка: {e}"]

def get_gov_benefits():
    try:
        url = 'https://www.gov.il/he/Departments/General/benefits-for-reservists'
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        benefits = soup.find_all('li', class_='benefit-item')
        return [f"{b.find('h4').text.strip()}\n{b.find('p').text.strip()}" for b in benefits[:3]]
    except Exception as e:
        return [f"Ошибка: {e}"]

# --- Языковая клавиатура ---

def language_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Русский"), KeyboardButton("עברית"))
    return kb

# --- Хендлеры ---

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, TEXT['ru']['welcome'], reply_markup=language_keyboard())

@bot.message_handler(func=lambda m: m.text in ["Русский", "עברית"])
def set_language(message):
    lang = 'ru' if message.text == "Русский" else 'he'
    user_lang[message.chat.id] = lang
    bot.send_message(message.chat.id, TEXT[lang]['language_selected'])
    bot.send_message(message.chat.id, TEXT[lang]['help'])

@bot.message_handler(commands=['help'])
def help_command(message):
    lang = user_lang.get(message.chat.id, 'ru')
    bot.send_message(message.chat.id, TEXT[lang]['help'])

@bot.message_handler(commands=['reservist'])
def reservist_info(message):
    lang = user_lang.get(message.chat.id, 'ru')
    bot.send_message(message.chat.id, TEXT[lang]['reservist_loading'])

    news = get_idf_news()
    benefits = get_gov_benefits()

    bot.send_message(message.chat.id, TEXT[lang]['reservist_title'])
    bot.send_message(message.chat.id, "\n\n".join(news))
    bot.send_message(message.chat.id, "\n\n".join(benefits))

@bot.message_handler(commands=['wounded'])
def wounded_info(message):
    lang = user_lang.get(message.chat.id, 'ru')
    bot.send_message(message.chat.id, TEXT[lang]['wounded'])

# --- Запуск ---
if __name__ == '__main__':
    print("Бот запущен с поддержкой двух языков.")
    bot.polling(none_stop=True)
