import config
import telebot
import DataBase
import os
import sqlite3

dbase = DataBase.DBase(config.database_name)

bot = telebot.TeleBot(config.token)

n = dbase.count_rows()



@bot.message_handler(commands=['pahosu06'])
def send_music(message):
    k = 0
    for i in os.listdir('music/'):
        k += 1
        if k > n:
            name = i[:-4]
            f = open('music/' + i, 'rb')
            msg = bot.send_voice(message.chat.id, f, None)
            tok = msg.voice.file_id
            with sqlite3.connect(config.database_name) as st:
                c = st.cursor()
                c.execute("""
                        INSERT INTO music
                        VALUES (?,?,?)
                        """, (k, tok, name))
        
if __name__ == '__main__':
    bot.polling(none_stop=True)
    
