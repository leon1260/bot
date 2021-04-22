import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('1666538048:AAHKz4ZFEVhuVPsxD2m9eJlQpqe9iEQX9W4')
ms = ''

con = sqlite3.connect("Db.sqlite")
cur = con.cursor()

users = cur.execute("""SELECT * FROM Users""").fetchall()
comp = cur.execute("""SELECT * FROM Composition""").fetchall()


# Вход в личный кабинет, регистрация и переадресация на скачивачивание
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global ms
    ms = message
    if '/log' in message.text:
        nomb = message.text[4:]
        nomb = int(nomb)
        if nomb <= len(users):
            isAdm = users[nomb - 1][4]
            if isAdm == 'True':
                bot.send_message(message.from_user.id, 'Введите вы хотите "Скачать" или "Загрузить"')
                bot.register_next_step_handler(message, DoworUp)
            else:
                keyboard = types.InlineKeyboardMarkup()
                key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
                keyboard.add(key_yes)
                key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
                keyboard.add(key_no)
                question = 'Хотите ли вы увидеть список произведений?'
                bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, 'Читательской карты с таким номером не существует')
            bot.register_next_step_handler(message, get_text_messages)
    elif '/reg' in message.text:
        bot.send_message(message.from_user.id, 'Введите ваши имя и фамилию.')
        bot.register_next_step_handler(message, Register)
    else:
        bot.send_message(message.from_user.id, 'Напишите /log и номер вашей читательской карты, чтобы получить доступ'
                                               'к скачиванию книг.')


def Register(message):
    name, suname = message.text.split()
    # реализовать добавление пользователя в базу данных
    bot.register_next_step_handler(message, get_text_messages)


# Вопрос о необходимости вывода списка произведений и перенаправление на скачивание
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global ms, comp
    if call.data == "yes":
        send = ''
        for i in range(len(comp)):
            send = send + '\n' + comp[i][1]
        bot.send_message(call.from_user.id, send)
        bot.send_message(call.from_user.id, 'Введите название произведения, которое хотите скачать')
        bot.register_next_step_handler(ms, Download)
    elif call.data == "no":
        bot.send_message(call.from_user.id, 'Введите название произведения, которое хотите скачать')
        bot.register_next_step_handler(ms, Download)


# Скачивание книг
def Download(message):
    global comp
    fl = False
    for i in range(len(comp)):
        if message.text.lower() in comp[i][1].lower():
            fl = True
            bot.send_message(message.from_user.id, comp[i][2])
            bot.send_message(message.from_user.id, 'Введите название произведения, которое хотите скачать')
            bot.register_next_step_handler(message, Download)
    if not fl:
        bot.send_message(message.from_user.id, 'Произведение не найдено.')
        bot.send_message(message.from_user.id, 'Введите название произведения, которое хотите скачать')
        bot.register_next_step_handler(message, Download)


# Опрос для админа скачивать он будет или загрузить
def DoworUp(message):
    if 'скачать' in message.text.lower():
        bot.send_message(message.from_user.id, 'Введите название произведения, которое вы хотите скачать')
        bot.register_next_step_handler(message, DownloadAdm)
    elif 'загрузить' in message.text.lower():
        bot.send_message(message.from_user.id, 'Введите название произведения и ссылку для скачивания')
        bot.register_next_step_handler(message, Upload)
    else:
        bot.send_message(message.from_user.id, 'Некоректный запрос.')
        bot.register_next_step_handler(message, DoworUp)


def Upload(message):
    name, link = message.text.split()
    # добавление книг в базу данных
    bot.send_message(message.from_user.id, 'Введите вы хотите "Скачать" или "Загрузить"')
    bot.register_next_step_handler(message, DoworUp)


# скачивание книг для админов
def DownloadAdm(message):
    global comp
    fl = False
    for i in range(len(comp)):
        if message.text.lower() in comp[i][1].lower():
            fl = True
            bot.send_message(message.from_user.id, comp[i][2])
            bot.send_message(message.from_user.id, 'Введите вы хотите "Скачать" или "Загрузить"')
            bot.register_next_step_handler(message, DoworUp)
    if not fl:
        bot.send_message(message.from_user.id, 'Произведение не найдено.')
        bot.send_message(message.from_user.id, 'Введите вы хотите "Скачать" или "Загрузить"')
        bot.register_next_step_handler(message, DoworUp)


bot.polling(none_stop=True, interval=0)
con.close()
