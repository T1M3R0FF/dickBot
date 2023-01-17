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
    bot.send_message(message.   chat.id, 'Welcome to the club, buddy!')


@bot.message_handler(commands=['measure'])
def measure(message):
    # проверка на дурака
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    # проверка на новую генерацию через сутки
    # если юзер существует и сутки не прошли
    if len(users_time) != 0 and len(users[message.from_user.username]) != 0 and time.perf_counter() - users_time[
        message.from_user.username] < 86400:
        bot.reply_to(message, f'{random.choice(dicks)} сегодня <b>{users[message.from_user.username][-1]}см</b>'
                              f'{random.choice(emojis)}', parse_mode='html')
        return True
    # если новый юзер, то дать замерить либо через сутки
    elif message.from_user.username not in users_time or (
            len(users_time) != 0 and time.perf_counter() - users_time[message.from_user.username] >= 86400):

        size = random.randint(0, 200)
        users_time.update({message.from_user.username: time.perf_counter()})
        users[message.from_user.username].append(size)
        bot.reply_to(message, f'{random.choice(dicks)} сегодня <b>{users[message.from_user.username][-1]}см</b>'
                              f'{random.choice(emojis)}', parse_mode='html')


@bot.message_handler(commands=['average'])
def average(message):
    total = 'Усреднённые жезлы на сегодняшний день:\n'
    if len(users) != 0:
        # сортировка выводимой строки
        sorted_users = dict(reversed(sorted(users.items(), key=lambda item: item[1])))
        # упаковка строки по каждому юзеру
        for key, value in sorted_users.items():
            total += f'@{str(key)}:  <b>{str(statistics.mean(value))} см</b>\n'
        bot.send_message(message.chat.id, total, parse_mode='html')


# замер у всех сразу
@bot.message_handler(commands=['all'])
def all_in(message):
    if len(users) == 0:
        bot.send_message(message.chat.id, 'Клуб опустел:(\nЗаходи, стань первым /start')
        return True
    else:
        everyone = 'Сегодняшние показатели следующие:\n'
        all_dict = {}
        for user in users.keys():
            # прошли сутки или новый юзер-генерим
            if user not in users_time or (user in users_time and time.perf_counter() - users_time[user] >= 86400):
                size = random.randint(0, 200)
                users_time.update({user: time.perf_counter()})
                users[user].append(size)
                all_dict.update({user: size})
                # пополняем список пользователей
                everyone += f'@{str(user)}:  <b>{str(size)} см</b>\n'

                # наоборот
            elif user in users_time and len(users[user]) != 0 and time.perf_counter() - users_time[user] < 86400:
                all_dict.update({user: users[user][-1]})
                # пополняем список пользователей
                everyone += f'@{str(user)}:  <b>{str(users[user][-1])} см</b>\n'
        # вывод
        bot.send_message(message.chat.id, everyone, parse_mode='html')


# выход из бота
@bot.message_handler(commands=['getout'])
def getout(message):
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты и так не в клубе, выйти не получится')
        return True
    else:
        if message.from_user.username in users_time:
            del users_time[message.from_user.username]
        del users[message.from_user.username]
        bot.send_message(message.chat.id, f'@{message.from_user.username} изволил покинуть наш клуб')


bot.polling(non_stop=True)
