---

```markdown
# 🪖 Многоязычный Telegram-бот помощи и поддержки солдат после войны  
# 🪖 Multilingual Telegram Bot for Post-War Soldier Support  
# 🪖 בוט טלגרם רב-לשוני לתמיכה וסיוע לחיילים אחרי המלחמה  

---

## 🇷🇺 Русский

### 📌 Описание

Этот бот предоставляет **поддержку солдатам после войны**:

- 📚 **FAQ** (на 3 языках)  
- ✍ Задание личного вопроса с ответом от ИИ  
- 👨‍⚕️ Связь с психологом, юристом, финансистом  
- 🌍 Интерфейс на русском, английском, иврите  
- 🤖 Ответы от OpenRouter API (без google/gemini-pro)  
- 💬 Вопросы пользователя сохраняются в базе FAQ  

---

### 🛠 Установка

```bash
git clone https://github.com/your_username/telegram-support-bot.git
cd telegram-support-bot
pip install -r requirements.txt
```

Создай файл `.env`:

```
BOT_TOKEN=твой_телеграм_токен
OPENROUTER_API_KEY=твой_ключ_OpenRouter
```

Запуск:

```bash
python main.py
```

---

## 🇺🇸 English

### 📌 Description

This bot provides **post-war soldier support**:

- 📚 **Multilingual FAQ**  
- ✍ Ask your own question and get AI-based answers  
- 👨‍⚕️ Contact psychologist, lawyer, or financial expert  
- 🌍 Interface in English, Russian, Hebrew  
- 🤖 Uses OpenRouter API (no Google Gemini)  
- 💬 User questions are stored and shown in FAQ  

---

### 🛠 Installation

```bash
git clone https://github.com/your_username/telegram-support-bot.git
cd telegram-support-bot
pip install -r requirements.txt
```

Create a `.env` file:

```
BOT_TOKEN=your_telegram_token
OPENROUTER_API_KEY=your_openrouter_key
```

Run:

```bash
python main.py
```

---

## 🇮🇱 עברית

### 📌 תיאור

הבוט מספק **תמיכה לחיילים אחרי מלחמה**:

- 📚 שאלות נפוצות ב-3 שפות  
- ✍ אפשרות לשאול שאלות אישיות ולקבל תשובות מבוססות AI  
- 👨‍⚕️ פנייה לפסיכולוג, עו"ד או יועץ כלכלי  
- 🌍 ממשק בעברית, רוסית ואנגלית  
- 🤖 שימוש ב־OpenRouter API (ללא Google Gemini)  
- 💬 שאלות המשתמש נשמרות ב־FAQ  

---

### 🛠 התקנה

```bash
git clone https://github.com/your_username/telegram-support-bot.git
cd telegram-support-bot
pip install -r requirements.txt
```

צור קובץ `.env`:

```
BOT_TOKEN=הטוקן_שלך_לטלגרם
OPENROUTER_API_KEY=המפתח_שלך_ל-OpenRouter
```

הרץ:

```bash
python main.py
```

---

## 📄 Структура проекта / Project Structure / מבנה פרויקט

```plaintext
├── main.py              # основной файл / main bot file / קובץ ראשי
├── .env                 # переменные окружения / environment variables / משתנים
├── requirements.txt     # зависимости / dependencies / תלויות
├── README.md            # описание проекта / project readme / קובץ תיאור
├── .gitignore           # исключения / git ignore file / קבצים להתעלמות
```

---
