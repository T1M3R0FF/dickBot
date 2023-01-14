import telebot
import random
import time
import statistics

bot = telebot.TeleBot('5706224983:AAFvcDUZGtn1_Fa4O7RU6AdBrynZcOsCAQc')

dicks = ['Твоя дилдосина', 'Твоя елда', 'Твой пенис', 'Твой хер',
         'Твоя залупа', 'Твой хуй', 'Твоя шишка', 'Твой нагибатель',
         'Твой эскалибур', 'Твоя палочка', 'Твой лысый Джонни Синс',
         'Твоя сигара', 'Твой питон', 'Твой писюн', 'Твой зверь',
         'Твой член', 'Твой хоботок', 'Твой маленький друг']
emojis = [' 😏', ' 😱', ' 😁', ' 😯', ' 🥰', ' 🤩', ' 😳', ' 😨', ' 😈', ' 🍌', ' 🌽', ' 🍆']

users = {}
users_time = {}


@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.username in users:
        bot.reply_to(message, "Ты уже в клубе")
        return True
    users.update({message.from_user.username: []})
    bot.send_message(message.chat.id, 'Welcome to the club, buddy!')


@bot.message_handler(commands=['measure'])
def measure(message):
    # проверка на дурака
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    # проверка на новую генерацию через сутки
    if len(users_time) != 0 and len(users[message.from_user.username]) != 0 and time.perf_counter() - users_time[
        message.from_user.username] < 86400:
        bot.reply_to(message, f'{random.choice(dicks)} сегодня <b>{users[message.from_user.username][-1]}см</b>'
                              f'{random.choice(emojis)}', parse_mode='html')
        return True

    elif message.from_user.username not in users_time or (
            len(users_time) != 0 and time.perf_counter() - users_time[message.from_user.username] >= 86400):

        size = random.randint(0, 200)
        users_time.update({message.from_user.username: time.perf_counter()})
        users[message.from_user.username].append(size)
        bot.reply_to(message, f'{random.choice(dicks)} сегодня <b>{users[message.from_user.username][-1]}см</b>'
                              f'{random.choice(emojis)}', parse_mode='html')


@bot.message_handler(commands=['average'])
def average(message):
    aver_dict = {}
    if len(users) != 0:
        for key, value in users.items():
            aver_dict.update({key: statistics.mean(value)})
        sorted_users = dict(reversed(sorted(aver_dict.items(), key=lambda item: item[1])))
        for key, value in sorted_users.items():
            bot.send_message(message.chat.id, f'Сводка по средним на сегодняшний день:\n'
                                              f'{key}: {value} см')


bot.polling(non_stop=True)
