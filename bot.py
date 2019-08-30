import telebot
import config
import random
import utils
from DataBase import DBase
from telebot import types
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands = ['game'])
def game(message):
    db = DBase(config.database_name)
    g = utils.get_rows_count()
    L = list(range(1, g + 1))
    random.shuffle(L)
    LL = []
    for i in range(4):
        row = db.select_single(L[i])
        LL.append(row[2])
    markup = utils.generate_markup(LL)
    ans = db.select_single(L[0])
    bot.send_voice(message.chat.id, ans[1], reply_markup=markup)
    utils.set_user_game(message.chat.id, ans[2], message.chat.username)
    db.close()

@bot.message_handler(commands = ['stats'])
def stats(message):
    user = message.chat.username
    r, w = utils.get_stats(user)
    bot.send_message(message.chat.id, 'Вы ответили на %i вопросов правильно и на %i - неправильно' % (r, w))


@bot.message_handler(func=lambda f: True, content_types=['text'])
def check_answer(message):
    answer = utils.get_answer_for_user(message.chat.id)
    if not answer:
        bot.send_message(message.chat.id, 'Что бы начать игру введите /game')
    else:
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            utils.set_ans(message.chat.username, 1, 0)
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            utils.set_ans(message.chat.username, 0, 1)
            bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        utils.finish_user_game(message.chat.id)

if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)
