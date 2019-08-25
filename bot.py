import os
import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands = ['test'])
def repeat_all_message(message):
    for file in os.listdir('music/'):
        if file.split('.')[-1] == 'mp3':
            f = open('music/'+file, 'rb')
            msg = bot.send_voice(message.chat.id, f, None) 
            bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id = msg.message_id)

if __name__ == '__main__':
    bot.polling(none_stop=True)


