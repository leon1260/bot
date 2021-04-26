import telebot
from telebot import types
import apiai
import json

from pprint import pprint
from validate_email import validate_email
import transliterate

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
        flag = False
        db_sess = db_session.create_session()

        for i in db_sess.query(User).filter(User.user_id == message.json['chat']['id']):
            flag = True
        if flag:
            bot.send_message(message.from_user.id, 'А я тебя уже знаю <3')
        else:
            human = User()
            human.name = message.json['chat']['first_name']
            human.user_id = message.json['chat']['id']
            human.subscription = 0
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


@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    # markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    # markup.add('1', '2')  # Имена кнопок
    # msg = bot.reply_to(message, 'Test text', reply_markup=markup)
    # # bot.register_next_step_handler(msg, process_step)

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

    elif message.text == 'Хочу загрузить книгу':
        bot.send_message(message.from_user.id, 'Нам нужен файл:')
        bot.register_next_step_handler(message, add_book)

    elif message.text == 'Хочу скачать книгу':
        bot.send_message(message.from_user.id, 'Напиши название книги:')
        bot.register_next_step_handler(message, find_book)

    else:
        # bot.send_message(1755857163, '/start')
        bot.send_message(message.from_user.id, message.text)


def add_book(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = r'db\books\book' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Осталось указать имя")
    bot.register_next_step_handler(message, add_book_db, src)


def add_book_db(message, src):
    db_sess = db_session.create_session()
    new_book = Book()
    new_book.name = message.text
    new_book.container = src
    db_sess.add(new_book)
    db_sess.commit()
    bot.reply_to(message, "Пожалуй, я сохраню это!")


name = ''


def find_book(message):
    global name
    name = message.text
    db_sess = db_session.create_session()
    btn_title_books = types.InlineKeyboardMarkup()

    title_books = []
    for k, book in enumerate(db_sess.query(Book).filter(Book.name.like(f"%{message.text}%"))):
        btn_title_books.add(types.InlineKeyboardButton(text=book.name, callback_data=f'{k}'))
        # title_books.append(book)

    bot.send_message(message.from_user.id, text='Книга?', reply_markup=btn_title_books)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(message):
    global name
    db_sess = db_session.create_session()
    title_books = []
    for book in db_sess.query(Book).filter(Book.name.like(f"%{name}%")):
        title_books.append(book)

    bot.send_document(message.from_user.id, open(title_books[int(message.data)].container, 'r', encoding='utf-8'))
    name = ''


# bot.set_webhook()
bot.polling(none_stop=True, interval=0)
