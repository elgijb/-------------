---

# 🧠 Многоязычный Telegram-бот помощи и поддержки солдат после войны 

## 📌 Описание проекта

Этот Telegram-бот предоставляет:
- Часто задаваемые вопросы (FAQ)
- Возможность задать свой вопрос и получить ответ от ИИ
- Обращение к специалистам: психолог, юрист, финансист
- Поддержку **трёх языков**: 🇷🇺 Русский, 🇺🇸 Английский, 🇮🇱 Иврит
- Интеграцию с **OpenRouter.ai API** (искусственный интеллект на основе Mixtral и Claude)
- Поддержку кнопок, лайков, многостраничного FAQ и истории вопросов

---

## 🚀 Как запустить

1. Установите зависимости:

```bash
pip install pyTelegramBotAPI python-dotenv requests
```

2. Создайте `.env` файл в корне проекта:

```env
BOT_TOKEN=ваш_токен_бота_от_Telegram
OPENROUTER_API_KEY=ваш_ключ_от_OpenRouter
```

3. Запустите бота:

```bash
python main.py
```

---

## 🔧 Функциональность

### 🗣️ Мультиязычность
При первом запуске бот предлагает выбрать язык (русский, английский, иврит). Все кнопки и сообщения адаптируются к выбранному языку.

### ❓ Часто задаваемые вопросы (FAQ)
- Выводит 10 базовых вопросов + добавленные пользователем
- Возможность поставить лайк
- Кнопка перехода к следующему вопросу
- Возврат в главное меню

### ✍ Задать свой вопрос
- Пользователь может задать вопрос в свободной форме
- Ответ формирует ИИ через OpenRouter.ai (Mixtral/Claude)
- Вопрос и ответ сохраняются в историю и показываются в общем FAQ

### 👨‍⚕️ Обратиться к специалисту
- Психологическая помощь
- Финансовая помощь
- Юридическая помощь  
Каждый тип предоставляет ссылку на проверенные ресурсы с кнопкой-переходом и кратким описанием.

---

## 📦 Структура проекта

```
📁 проект/
├── main.py                # Основной файл Telegram-бота
├── .env                   # Конфиденциальные переменные окружения
├── .gitignore             # Исключения для git
└── README.md              # Описание проекта
```

---

## 🔐 Защита данных

- Все токены хранятся в `.env`
- `.env` добавлен в `.gitignore`

---

## 💡 Пример API-запроса

Используется OpenRouter API (совместим с OpenAI):

```python
import requests

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
data = {
    "model": "mistralai/mixtral-8x7b",
    "messages": [{"role": "user", "content": "Привет, как дела?"}]
}
response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
print(response.json()['choices'][0]['message']['content'])
```

---

## 🛠 Возможности для доработки

- Добавить кнопки «Поделиться» или «Оценить бота»
- Расширить базу вопросов FAQ
- Добавить админ-панель


Вот полный, подробный `README.md` на английском языке, переведённый со всех разделов, которые ты делал:

---

# 🪖 **Multilingual Telegram Bot for Post-War Soldier Support and Assistance**

## 📌 Project Description

This Telegram bot is designed to **support soldiers after military operations**, offering emotional, legal, and financial help. It provides:

- 📚 A list of **Frequently Asked Questions** (FAQ) in three languages  
- ✍️ A feature to **ask personal questions** and receive smart AI-based answers  
- 👨‍⚕️ An option to **contact a specialist**: psychologist, lawyer, or financial advisor  
- 🌍 **Multilingual interface**: fully supports Russian, English, and Hebrew  
- 🤖 Uses **OpenRouter.ai API** (with models *excluding google/gemini-pro*) for smart, multilingual responses  
- 💬 Keeps track of user questions and displays them as part of future FAQ  

---

## 🧠 Technologies Used

- **Python 3.11+**
- [pyTelegramBotAPI (telebot)](https://github.com/eternnoir/pyTelegramBotAPI)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [OpenRouter.ai](https://openrouter.ai) for LLM-powered responses

---

## 🛠 Installation Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/your_username/telegram-support-bot.git
cd telegram-support-bot
```

2. **Install required libraries:**

```bash
pip install -r requirements.txt
```

3. **Set up your environment variables:**

Create a `.env` file in the root directory with the following content:

```
BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
```

4. **Run the bot:**

```bash
python main.py
```

---

## 🌐 Languages Supported

The bot interface, FAQ section, and answers all work in:

- 🇷🇺 Russian  
- 🇺🇸 English  
- 🇮🇱 Hebrew

Users can switch languages at any time using the "Change Language" button.

---

## 🤖 AI Integration

The bot uses [OpenRouter.ai](https://openrouter.ai)'s API for answering user questions. You can choose among free models that support multilingual output (excluding Google Gemini Pro).

### Example Models (Free and support Hebrew, English, Russian):

- `mistralai/mixtral-8x7b`
- `anthropic/claude-3-haiku`

---

## 🧑‍⚕️ Specialist Access

In the "Contact a Specialist" section, users can choose:

- 🧠 **Psychological help**  
- ⚖️ **Legal help**  
- 💰 **Financial help**

Each option leads to relevant online resources with clickable links for direct access.

---

## 📄 File Structure

```plaintext
├── main.py              # Main bot script
├── .env                 # API tokens
├── requirements.txt     # Dependencies
├── README.md            # You are here
└── .gitignore           # Ignored files
```

---

## 🧾 .gitignore Example

```gitignore
.env
__pycache__/
*.pyc
.DS_Store
.idea/
*.log
```

---

## 📬 Contact

Want to improve or contribute? Feel free to fork and send a pull request.

For any help, you can contact the maintainer via Telegram or GitHub.


Вот полный перевод `README.md` на **иврит** — ничего не потеряно, всё адаптировано и оформлено по структуре:

---

# 🪖 **בוט טלגרם רב-לשוני לתמיכה וסיוע לחיילים אחרי המלחמה**

## 📌 תיאור הפרויקט

הבוט נועד לספק **תמיכה מקיפה לחיילים אחרי שירות צבאי או מלחמה** ומציע:

- 📚 רשימת **שאלות נפוצות (FAQ)** בשלוש שפות  
- ✍️ אפשרות **לשאול שאלות אישיות** ולקבל תשובות מבוססות בינה מלאכותית  
- 👨‍⚕️ אפשרות **לפנות למומחה**: פסיכולוג, עו״ד או יועץ פיננסי  
- 🌍 **ממשק רב-לשוני**: תומך בעברית, רוסית ואנגלית  
- 🤖 שימוש ב-**OpenRouter.ai API** (ללא google/gemini-pro) לתשובות חכמות  
- 💬 שמירת שאלות המשתמש והצגתן כחלק מה-FAQ בעתיד  

---

## 🧠 טכנולוגיות בשימוש

- **Python 3.11+**
- [pyTelegramBotAPI (telebot)](https://github.com/eternnoir/pyTelegramBotAPI)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [OpenRouter.ai](https://openrouter.ai) לקבלת תשובות בינה מלאכותית

---

## 🛠 הוראות התקנה

1. **שכפל את הריפוזיטורי:**

```bash
git clone https://github.com/your_username/telegram-support-bot.git
cd telegram-support-bot
```

2. **התקן את התלויות:**

```bash
pip install -r requirements.txt
```

3. **צור קובץ סביבה (.env):**

```
BOT_TOKEN=הטוקן_שלך_לטלגרם
OPENROUTER_API_KEY=המפתח_שלך_ל-OpenRouter
```

4. **הפעל את הבוט:**

```bash
python main.py
```

---

## 🌐 שפות נתמכות

הממשק, ה-FAQ והתשובות פועלים בשלוש שפות:

- 🇮🇱 עברית  
- 🇷🇺 רוסית  
- 🇺🇸 אנגלית  

ניתן להחליף שפה בכל עת על ידי לחיצה על "שנה שפה".

---

## 🤖 אינטגרציית בינה מלאכותית

הבוט משתמש ב-API של [OpenRouter.ai](https://openrouter.ai) כדי להשיב על שאלות המשתמש.  
הוא תומך במודלים חינמיים עם תמיכה בעברית, אנגלית ורוסית  
(**ללא** השימוש ב־Google Gemini).

### מודלים מומלצים:

- `mistralai/mixtral-8x7b`
- `anthropic/claude-3-haiku`

---

## 🧑‍⚕️ פנייה למומחה

תחת האפשרות "פנייה למומחה", ניתן לבחור:

- 🧠 **עזרה פסיכולוגית**  
- ⚖️ **עזרה משפטית**  
- 💰 **סיוע כלכלי**  

הבוט מספק קישורים ישירים לאתרים רשמיים ולמשאבים שימושיים.

---

## 📄 מבנה קבצים

```plaintext
├── main.py              # קובץ ראשי של הבוט
├── .env                 # משתני סביבה
├── requirements.txt     # תלויות
├── README.md            # הקובץ הזה
└── .gitignore           # קבצים להתעלמות בגיט
```

---

## 🧾 .gitignore לדוגמה

```gitignore
.env
__pycache__/
*.pyc
.DS_Store
.idea/
*.log
```

---

## 📬 יצירת קשר

רוצה לשפר או לתרום? מוזמן לבצע fork ולשלוח pull request.

לסיוע נוסף, אפשר לפנות למתחזק הבוט דרך טלגרם או GitHub.

---

Если хочешь, могу теперь упаковать все три README в один многоязычный вариант (с переключением по заголовкам)?