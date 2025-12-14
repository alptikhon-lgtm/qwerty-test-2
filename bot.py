import pandas
from telebot import TeleBot, types
import threading
from datetime import datetime
import time
import random
from urllib.parse import quote_plus
import requests
import Test2
BOTTOKEN = '8229981124:AAEuU5RpZKAYKosrVG2zfd3LHL6Ju-dXslc'
bot = TeleBot(BOTTOKEN)
days_of_week = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье"
}

users= set()

@bot.message_handler(commands=['start'])
def sf(m):
    bot.send_sticker(m.chat.id, "CAACAgIAAxkBAAEPwBdpEqiSxlRd_H20g8brjTsUU9nWFAACBQADwDZPE_lqX5qCa011NgQ")
    bot.send_message(m.chat.id, "привет это бот тихона\n"
    "узнай что я делаю командой /info")

@bot.message_handler(commands=["info"])
def info(m):
   kl1 = types.InlineKeyboardMarkup()
   kl2 = types.ReplyKeyboardMarkup()

   bt1 = types.InlineKeyboardButton("/notice", callback_data="/notice")
   bt2 = types.InlineKeyboardButton("/unsub", callback_data="/unsub",)
   bt3 = types.InlineKeyboardButton("/image", callback_data="/image")
   bt4 = types.InlineKeyboardButton("/parser", callback_data="/parser" )

   bt5 = types.KeyboardButton("/notice")
   bt6 = types.KeyboardButton("/unsub")
   bt7 = types.KeyboardButton("/image")
   bt8 = types.KeyboardButton("/parser")

   kl1.add(bt1, bt2, bt3, bt4)
   kl2.add(bt5, bt6, bt7, bt8)

   bot.send_message(m.chat.id, "Список команд бота:\n"
                               "/start - приветсвтие\n"
                               "/info - все команды бота\n"
                               "/notice - подписаться на уведомления\n"
                               "/unsub - отписаться от уведомлений\n"
                               "/image - сгенерировать картинку по текстовому запросу\n"
                               "/parser - получить подборку товаров электроники по запросу", reply_markup=kl1)

   bot.send_message(m.chat.id, "кнопки есть✅", reply_markup=kl2)

@bot.message_handler(commands=["notice"])
def notice(m):
    users.add(m.chat.id)
    bot.send_message(m.chat.id,"Вы подписались на уведомления✅")


@bot.message_handler(commands=["unsub"])
def unsub(m):
    users.discard(m.chat.id)
    bot.send_message(m.chat.id, "Вы отписались от уведомлений")


@bot.message_handler(commands=['image'])
def sendImg(m):
    bot.reply_to(m, "Hello✅")
    bot.send_sticker(m.chat.id, "CAACAgIAAxkBAAEPwBdpEqiSxlRd_H20g8brjTsUU9nWFAACBQADwDZPE_lqX5qCa011NgQ")
    bot.send_message(m.chat.id, "приветствуем вас в image генератор\n"
    "узнай что я делаю командой /info1")
@bot.message_handler(commands=["info1"])
def info(m):
    bot.send_message(m.chat.id, "Список команд бота:\n"
                                "прочти инструкцию не нажимай бездумно img /img(что ты хочешь на пример /img car)(пиши на англ.)-генерация картинок")
@bot.message_handler(commands=['img'])
def sendImg(m):
    bot.reply_to(m, "Генерирую")
    prompt = m.text.partition(' ')[2].strip()
    seed = random.randint(0, 2_000_000_000)
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=768&height=768&seed={seed}&n=1"
    r = requests.get(url, timeout=90, allow_redirects=True)
    bot.send_photo(m.chat.id, r.content, caption="Готово ✅")


bot.infinity_polling()


def get_beautiful_column_name(column: str) -> str:
    """Преобразует названия колонок в красивые"""
    column_names = {
        'Time': '🕒 Время',
        'Subject': '📖 Предмет',
        'Teacher': '👨‍🏫 Преподаватель',
        'Room': '🏫 Аудитория',
    }
    return column_names.get(column, column)


def setShedul(user):
    today_weekday = datetime.today().weekday() + 1  # 1–7
    # Суббота
    if today_weekday == 6:
        bot.send_message(
            user,
            "🎉 *Суббота* - занятий нет!\nМожно отдохнуть! 😊",
            parse_mode='Markdown'
        )
        return

    # Воскресенье
    if today_weekday == 7:
        bot.send_message(
            user,
            "🌟 *Воскресенье* - занятий нет!\nИдеальный день для отдыха! ☀️",
            parse_mode='Markdown'
        )
        return

    df = pandas.read_excel('schedule.xlsx')
    today_schedule = df[df['Day'] == today_weekday]

    if today_schedule.empty:
        day_name = days_of_week.get(today_weekday, "сегодня")
        bot.send_message(
        user,
        f"🎉 *{day_name.upper()}* - занятий нет!\nОтличный день для саморазвития! 📚",
        parse_mode='Markdown'
    )
        return

    day_name = days_of_week.get(today_weekday, "сегодня")
    response = f"📚 *РАСПИСАНИЕ НА {day_name.upper()}* 📚\n\n"

    for _, row in today_schedule.iterrows():
        response += "▫️" * 20 + "\n"

    for column, value in row.items():
        if column != 'Day' and pandas.notna(value) and str(value).strip() != '':
            column_name = get_beautiful_column_name(column)
            response += f"*{column_name}:* {value}\n"

    response += "\n" + "═" * 30 + "\n\n"

    total_lessons = len(today_schedule)
    response += f"📊 *Всего пар: {total_lessons}*"

    bot.send_message(user, response, parse_mode='Markdown')


def check_time():
    while True:
      now=datetime.now()
      if now.hour == 19 and now.minute == 42:
          for user in list(users):
              setShedul(user)

      time.sleep(10)

def start_scheduler():
    scheduler_thread = threading.Thread(target=check_time)
    scheduler_thread.daemon = True  # фоновый поток
    scheduler_thread.start()


if __name__ == "__main__":
    print("Бот запущен...")
    start_scheduler()

    bot.infinity_polling()




