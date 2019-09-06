import telebot
import config
import random
import time
from math import trunc
import utils
import snake
from DataBase import DBase
from telebot import types
bot = telebot.TeleBot(config.token)

d = 0
kk = 0

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
    bot.send_voice(message.chat.id, ans[1], reply_markup=markup, reply_to_message_id = message.message_id)
    utils.set_user_game(message.chat.id, ans[2], message.chat.username)
    db.close()

@bot.message_handler(commands = ['snake'])
def snake_game(message):
    global d
    global kk
    kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text = 'up', callback_data = 'u')
    kb.add(button)
    button1 = types.InlineKeyboardButton(text = 'right', callback_data = 'r')
    button = types.InlineKeyboardButton(text = 'left', callback_data = 'l')
    kb.row(button, button1)
    button = types.InlineKeyboardButton(text = 'down', callback_data = 'd')
    kb.add(button)
    F, S, d, h, p = snake.init()
    t = time.clock()
    tr = 1
    kk = 1
    txt = ''
    for i in F:
        for j in i:
            txt = txt + j
        txt = txt + '\n'
    msg = bot.send_message(chat_id = message.chat.id, text = txt, reply_markup = kb)
    while tr:
        tt = trunc(time.clock() * 1)
        h = S[0]
        if tt > t:
            t += 1
            kk = 1
            tr, F, S, d, h, p = snake.step(F, S, d, h, p)
            txt = ''
            for i in F:
                for j in i:
                    txt = txt + j
                txt = txt + '\n'
            bot.edit_message_text(chat_id = msg.chat.id, message_id = msg.message_id, text = txt, reply_markup = kb)
    d = 0

        

@bot.message_handler(commands = ['stats'])
def stats(message):
    user = message.chat.username
    r, w = utils.get_stats(user)
    bot.send_message(message.chat.id, 'Вы ответили на %i вопросов правильно и на %i - неправильно' % (r, w))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        global d
        global kk
        if not d:
            check_answer(call.message)
        elif call.data == 'u' and kk and d != 'd':
            d = 'u'
            kk = 0
        elif call.data == 'd' and kk and d != 'u':
            d = 'd'
            kk = 0
        elif call.data == 'l' and kk and d != 'r':
            d = 'l'
            kk = 0
        elif call.data == 'r' and kk and d != 'l':
            d = 'r'
            kk = 0 


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
