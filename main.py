from api.canvas import CanvasAPI
import os
import telebot
from env import BOT_TOKEN
from env import CANVAS_COURSE_ID
from env import MINUTES
from env import REFRESH_TIME
from env import CHAT_ID
from datetime import datetime as dt
from datetime import timezone
from dateutil.relativedelta import relativedelta as rd
import time

def date_parser(stringdate):
    try:
        stringdate = stringdate.replace('Z', '+00:00')
        datetime = dt.fromisoformat(stringdate)
        cond = (dt.now(timezone.utc) < datetime < (dt.now(timezone.utc) + rd(minutes = MINUTES)))
    except:
        cond = False
    return cond

def get_quizzes(course):
    quizzes = course.Quizzes.info.df
    if quizzes is None:
        return None
    quizzes = quizzes.to_numpy()
    # due_at, unlock_at, lock_at
    quizzes = list(filter(lambda x: (date_parser(x[8]) or date_parser(x[9]) or date_parser(x[10])) , quizzes))
    return quizzes

def convert_utc_to_local(utc_datetime):
    try:
        stringdate = utc_datetime.replace('Z', '+00:00')
        datetime = dt.fromisoformat(stringdate)
        return datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)
    except:
        return utc_datetime

def format_quiz(quiz):
    msg = f'''You have an upcoming quiz:
    Title: {quiz[1]}
    Due at: {convert_utc_to_local(quiz[8])}
    Unlock at: {convert_utc_to_local(quiz[9])}
    Lock at: {convert_utc_to_local(quiz[10])}
    HTML URL: {quiz[2]}
    '''
    return msg

def handle_quizzes(canvas):
    quizzes = get_quizzes(canvas)
    print('quizzes:', quizzes)
    if quizzes == None:
        bot.send_message(CHAT_ID, 'You do not have access to this course', parse_mode="Markdown")
    
    for i in quizzes:
        bot.send_message(CHAT_ID, format_quiz(i), parse_mode="Markdown")
        
bot = telebot.TeleBot(BOT_TOKEN)

if __name__ == "__main__":
    global canvas
    canvas = CanvasAPI(CANVAS_COURSE_ID)
    canvas.login()
        
    # Comment out this while loop to use the handler method below instead
    while True:
        print('Checking for quizzes')
        handle_quizzes(canvas)
        time.sleep(REFRESH_TIME)
        
    # Use this handler by commenting out the above while loop
    @bot.message_handler(commands=['quiz'])
    def get_quiz(message):
        text = "Enter course ID you want to get quiz for:"
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, get_id)
    def get_id(message):
        new_id = message.text
        try:
            num = int(new_id)
        except ValueError:
            text = "Enter a valid course ID"
            bot.register_next_step_handler(text, get_id)
        try:
            global canvas 
            canvas = CanvasAPI(num)
            canvas.login()
        except:
            text = "Enter a valid course ID"
            bot.register_next_step_handler(text, get_id)
        msg = 'Getting quizzes for course: ' + str(num)
        msg = bot.reply_to(message, msg)
        handle_quizzes(canvas)
    bot.infinity_polling()