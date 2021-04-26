import telebot
import apiai
import json

from pprint import pprint
from validate_email import validate_email

from data.books import Book
from data.users import User
from data import db_session

with open('data/replies.txt', 'r', encoding='utf-8') as f:
    data = f.read().split('\n\n')
    print(data)
    answers = {
        '/login': [data[0], ]
    }

bot_token = '1730695422:AAHqBhhtk-P6hxbTwuCnLBRg0-IywSZMyH0'
bot = telebot.TeleBot(bot_token)

# web_hook = f'https://yourwebhookserver.com/{bot_token}'

commands = ['/start', '/help', '/login - зарегистрироваться']
db_session.global_init('db/library.db')

info = [False, []]


# Приветствие //


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global info
    if message.text == '/help':
        bot.send_message(message.from_user.id, 'Доступные команды:\n' + "\n".join(commands))


@bot.message_handler(commands=['login'])
def start_login(message):
    if message.text == '/login':
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.user_id == message.json['chat']['id']):
            bot.send_message(message.from_user.id, 'А я тебя уже знаю <3')
        else:
            human = User()
            human.name = message.json['chat']['first_name']
            human.user_id = message.json['chat']['id']
            db_sess.add(human)
            db_sess.commit()
            bot.send_message(message.from_user.id, answers[message.text][0])


# def get_name(message, human):
#     # if validate_email(message.text, verify=True):
#     if 'i' == 'i':
#         human.email = message.text
#         bot.register_next_step_handler(message, get_password, human)
#     else:
#         bot.send_message(message.from_user.id, 'Ваш email адрес недействителен лол')
#
#
# def get_password(message, human):
#     human.set_password(message.text)
#     if human.check_password(message.text):
#         db_sess = db_session.create_session()
#         db_sess.add(human)
#         db_sess.commit()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    pprint(message.json)
    print()
    #Вход в личный кабинет и регистрация
    if message.text == 'Кто я?':
        find = False
        db_sess = db_session.create_session()
        for i in db_sess.query(User).filter(User.user_id == message.json['chat']['id']):
            bot.send_message(message.from_user.id, f'О, это же ты, {i.name}')
            find = True
        if not find:
            bot.send_message(message.from_user.id, 'Я тебя не знаю :(, напиши мне /login')
    elif message.text == 'Можно книгу?':
        bot.send_message(message.from_user.id, 'Напиши название книги:')
        bot.register_next_step_handler(message, find_book)

    else:
        # bot.send_message(1755857163, '/start')
        bot.send_message(message.from_user.id, message.text)


def find_book(message):
    db_sess = db_session.create_session()
    for book in db_sess.query(Book).filter(Book.name.like(f"%{message.text}%")):
        bot.send_document(message.from_user.id, open(book.container, 'r', encoding='utf-8'))


# bot.set_webhook()
bot.polling(none_stop=True, interval=0)
