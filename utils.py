import shelve
from random import shuffle
from telebot import types
from DataBase import DBase
from config import shelve_name, database_name, stats_name

def count_rows():
    db = DBase(database_name)
    #print(db.cursor)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rowsnum


def get_rows_count():
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum


def set_user_game(chat_id, estimated_answer, user):
    st = DBase(stats_name)
    st.set_user(user)
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id): 
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]

def get_answer_for_user(chat_id):
     with shelve.open(shelve_name) as storage:
         try:
             answer = storage[str(chat_id)]
             return answer
         except:
             return None
            
def set_ans(user, r, w):
    st = DBase(stats_name)
    st.set_ans(user, r, w)
    

def generate_markup(answers):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    shuffle(answers)
    for i in answers:
        markup.add(i)
    return markup

def get_stats(user):
    st = DBase(stats_name)
    r, w = st.stats(user)
    return r, w
