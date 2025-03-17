import telebot
from telebot.types import Message

from config import TOKEN
from parse import parse_news, parse_description
from keyboards import make_row_keyboard

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def cmd_start(message: Message):
    news = parse_news()
    if isinstance(news, dict):
        for i, new in news.items():
            title = new.get('title')
            time = new.get('time')
            bot.send_message(message.chat.id, f"ID: {i}\nЗаголовок: {title}\nВремя: {time}\n")
        choice = bot.send_message(message.chat.id, "Выберите ID новости")
        bot.register_next_step_handler(choice, handler, news)
    else:
        bot.send_message(message.chat.id, "Попробуйте еще раз")


def handler(message: Message, news):
    if message.text.isdigit() and 0 < int(message.text) <= 20:
        news_id = int(message.text)
        choice = bot.send_message(message.chat.id, "Можете посмотреть фото или описание", reply_markup=make_row_keyboard(["Description", "Photo"]))
        bot.register_next_step_handler(choice, second_handler, news_id, news)
    else:
        bot.send_message(message.chat.id, "Попробуйте еще раз")


def second_handler(message: Message, news_id, news):
    if message.text.lower() == 'description':
        bot.send_message(message.chat.id, f'Описание: {parse_description(news[news_id].get("link"))}\n'
                                          f'Ссылка описания: {news[news_id].get("link")}', reply_markup=make_row_keyboard(["Quit"]))
    elif message.text.lower() == 'photo':
        bot.send_photo(message.chat.id, news[news_id].get("photo"), f'Ссылка на фото: {news[news_id].get("photo")}', reply_markup=make_row_keyboard(["Quit"]))
    else:
        bot.send_message(message.chat.id, 'Попробуйте еще раз')


@bot.message_handler(content_types=['text'])
def cmd_quit(message: Message):
    if message.text.lower() == 'quit':
        bot.send_message(message.chat.id, "До свидания", reply_markup=telebot.types.ReplyKeyboardRemove())


bot.polling(none_stop=True)


