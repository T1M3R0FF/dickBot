import telebot
import random
import time
import statistics
import schedule
from telebot import types
from threading import Thread

bot = telebot.TeleBot('5706224983:AAFvcDUZGtn1_Fa4O7RU6AdBrynZcOsCAQc')

dicks = ['Твоя дилдосина', 'Твоя елда', 'Твой пенис', 'Твой хер',
         'Твоя залупа', 'Твой хуй', 'Твоя шишка', 'Твой нагибатель',
         'Твой экскалибур', 'Твоя палочка', 'Твой лысый Джонни Синс',
         'Твоя сигара', 'Твой питон', 'Твой писюн', 'Твой зверь',
         'Твой член', 'Твой хоботок', 'Твой маленький друг']
emojis = [' 😏', ' 😱', ' 😁', ' 😯', ' 🥰', ' 🤩', ' 😳', ' 😨', ' 😈', ' 🍌', ' 🌽', ' 🍆']

temp_set = []  # для проверки айди пользователя в plus() и minus()
users = {}
users_time = {}
users_bonus = {}
users_scale = {}
gays = {}
gays_time = {}
average_dicks = {}
gayresist_d = {}
check_battle = {}
battle_time = 0
chat_id = 0
resist_time = 0


@bot.message_handler(commands=['help'])
def manual(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Скрыть', callback_data='hide')
    markup.add(button1)
    bot.reply_to(message, 'Здарова, пробежимся по командам.\n'
                          'Через /start ты заходишь в бота и можешь использовать его команды. /measure, как и /gay'
                          ' просто измеряют член и насколько ты гей соответственно(измерять можно раз в сутки,'
                          ' если сутки не прошли, высветится то же значение), эти значения можно усреднить через'
                          ' /average и /gayaverage, но /average высчитывается не просто так. Каждый раз, '
                          'делая новый замер члена, тебе падает на бонусный счет(/balance) 10% от размера. Эти бонусы'
                          ' можно использовать двумя способами: либо прибавить кому то сантиметры к СРЕДНЕМУ значению'
                          '(/plus), либо убавить(/minus), в том числе и себе. То число, сколько тебе накинули в сумме,'
                          ' будет каждый раз вычитаться или прибавляться к среднему значению. Пример: по итогу 3-х дней'
                          ' среднее значение у тебя 50 см, но тебе в сумме накинули на -15(посмотреть, сколько тебе'
                          ' накинули можно через /scale). Таким образом, среднее у тебя считается как 50-15=35 см. На'
                          ' следующий день ты сделал замер, и среднее у тебя стало 60 см, но в scale до сих пор -15,'
                          ' поэтому среднее будет 60-15=45 см. Кажется, всё.\n'
                          ' /all замеряет сразу у всех, кто прожал старт, /getout - выход из бота. Веселитесь!',
                 reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    global chat_id
    chat_id = message.chat.id
    if message.from_user.username in users:
        bot.reply_to(message, "Ты уже в клубе", parse_mode=None)
        return True
    users.update({message.from_user.username: []})
    gays.update({message.from_user.username: []})
    users_bonus.update({message.from_user.username: 0})
    users_scale.update({message.from_user.username: 0})
    gayresist_d.update({message.from_user.username: {}})
    bot.send_message(message.chat.id, 'Welcome to the club, buddy!')


@bot.message_handler(commands=['measure'])
def measure(message):
    # проверка на дурака
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    # проверка на новую генерацию через сутки
    # если юзер существует и сутки не прошли
    if len(users_time) != 0 and len(users[message.from_user.username]) != 0 \
            and time.perf_counter() - users_time[message.from_user.username] < 86400:
        bot.reply_to(message, f'{random.choice(dicks)} сегодня'
                              f' <b>{users[message.from_user.username][-1]}см</b>'
                              f'{random.choice(emojis)}', parse_mode='html')
        return True
    # если новый юзер, то дать замерить либо через сутки
    elif message.from_user.username not in users_time or (
            len(users_time) != 0 and time.perf_counter() -
            users_time[message.from_user.username] >= 86400):

        size = random.randint(0, 200)
        users_time.update({message.from_user.username: time.perf_counter()})
        users[message.from_user.username].append(size)
        average_dicks.update({message.from_user.username: statistics.mean(users[message.from_user.username])})
        users_bonus[message.from_user.username] += size // 10
        bot.reply_to(message, f'{random.choice(dicks)} сегодня <b>{users[message.from_user.username][-1]}см</b>'
                              f'{random.choice(emojis)}', parse_mode='html')


@bot.message_handler(commands=['average'])
def average(message):
    # проверка на дурака
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    total = 'Усреднённые жезлы на сегодняшний день:\n'
    if len(users) != 0:
        # сортировка выводимой строки
        sorted_users = dict(reversed(sorted(average_dicks.items(), key=lambda item: item[1])))
        # упаковка строки по каждому юзеру
        for key, value in sorted_users.items():
            total += f'@{str(key)}:  <b>{str(value + users_scale[key])} см</b>\n'
        bot.send_message(message.chat.id, total, parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Клуб все еще пуст, заходи /start')


# замер у всех сразу
@bot.message_handler(commands=['all'])
def all_in(message):
    # проверка на дурака
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True

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
                average_dicks.update({user: statistics.mean(users[user])})
                users_bonus[message.from_user.username] += size // 10
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


# гейметр
@bot.message_handler(commands=['gay'])
def gay(message):
    # проверка на дурака
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True

    if len(gays_time) != 0 and len(gays[message.from_user.username]) != 0 \
            and time.perf_counter() - gays_time[message.from_user.username] < 86400:
        bot.reply_to(message, f'@{message.from_user.username} сегодня гей на'
                              f' <b>{gays[message.from_user.username][-1]}%</b>', parse_mode='html')
        return True
    # если новый юзер или прошли сутки, то дать замерить
    elif message.from_user.username not in gays_time or (
            len(gays_time) != 0 and time.perf_counter() - gays_time[message.from_user.username] >= 86400):

        size = random.randint(0, 100)
        gays_time.update({message.from_user.username: time.perf_counter()})
        gays[message.from_user.username].append(size)
        bot.reply_to(message, f'@{message.from_user.username} сегодня гей на'
                              f' <b>{gays[message.from_user.username][-1]}%</b>', parse_mode='html')


# средние геи
@bot.message_handler(commands=['gayaverage'])
def gayaverage(message):
    # проверка на дурака
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True

    total = 'Посмотрим на латентных наших средних:\n'
    if len(gays) != 0:
        # сортировка выводимой строки
        sorted_gays = dict(reversed(sorted(gays.items(), key=lambda item: item[1])))
        # упаковка строки по каждому юзеру
        for key, value in sorted_gays.items():
            total += f'@{str(key)}: <b>{str(statistics.mean(value))} %</b>\n'
        bot.send_message(message.chat.id, total, parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Клуб все еще пуст, заходи /start')


# выход из бота
@bot.message_handler(commands=['getout'])
def getout(message):
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты и так не в клубе, выйти не получится')
        return True
    else:
        if message.from_user.username in users_time:
            del users_time[message.from_user.username]

        if message.from_user.username in gays_time:
            del gays_time[message.from_user.username]

        if message.from_user.username in average_dicks:
            del average_dicks[message.from_user.username]

        del gays[message.from_user.username]
        del users[message.from_user.username]
        del users_bonus[message.from_user.username]
        del users_scale[message.from_user.username]
        bot.send_message(message.chat.id, f'@{message.from_user.username} изволил покинуть наш клуб')


# проверка баланса
@bot.message_handler(commands=['balance'])
def balance(message):
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    bot.reply_to(message, f'Ваш текущий баланс: <b>{users_bonus[message.from_user.username]} очков</b>',
                 parse_mode='html')


# прибавить кому-то см к среднему
@bot.message_handler(commands=['plus'])
def plus(message):
    name = message.from_user.username
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    if len(temp_set) != 0:
        msg = bot.send_message(message.chat.id, f'Подожди, пока {temp_set[0]} завершит операцию')
        bot.register_next_step_handler(msg, add)
    else:
        temp_set.append(name)
        msg1 = bot.send_message(message.chat.id, 'Введите ник и число через пробел - кому и сколько хотите накинуть.'
                                                 '(Jimmythedoc 10)\n'
                                                 'Для отмены нажмите /cancel')
        bot.register_next_step_handler(msg1, add)


def add(message):
    if message.from_user.username in temp_set:
        if message.text == '/cancel':
            bot.reply_to(message, 'Галя, отмена!')
            temp_set.clear()
            return True
        text = message.text.split(' ')
        if len(text) != 2 or not text[-1].isdigit():
            bot.send_message(message.chat.id, 'Некорректный ввод, попробуйте еще раз /plus')
            temp_set.clear()
            return True
        if len(text) == 2 and text[-1].isdigit():
            nickname = text[-2]
            inches = int(text[-1])
            if nickname not in users_bonus:
                mess0 = bot.send_message(message.chat.id, f'Пользователь {nickname} еще не клубе, попробуйте еще раз')
                bot.register_next_step_handler(mess0, add)
            elif inches <= users_bonus[message.from_user.username]:
                users_bonus[message.from_user.username] -= inches
                users_scale[nickname] += inches
                bot.send_message(message.chat.id, f'Успешно накинул пользователю <b>{nickname} {inches} см.</b>',
                                 parse_mode='html')
                temp_set.clear()
            elif inches > users_bonus[message.from_user.username]:
                bot.send_message(message.chat.id, 'У вас нет столько бонусов, попробуйте заново')
                temp_set.clear()
                return True
        else:
            bot.register_next_step_handler(message, add)


# отнять у кого-то см от среднего
@bot.message_handler(commands=['minus'])
def minus(message):
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    if len(temp_set) != 0:
        msg = bot.send_message(message.chat.id, f'Подожди, пока {temp_set[0]} завершит операцию')
        bot.register_next_step_handler(msg, remove)
    if message.from_user.username in users:
        temp_set.append(message.from_user.username)
        message1 = bot.reply_to(message, 'Введите ник и число через пробел - кому и сколько хотите убавить.'
                                         '(Jimmythedoc 10)\n'
                                         'Для отмены нажмите /cancel')
        bot.register_next_step_handler(message1, remove)


def remove(message):
    global resist_time
    if message.from_user.username in temp_set:
        if message.text == '/cancel':
            bot.reply_to(message, 'Галя, отмена!')
            temp_set.clear()
            return True
        text = message.text.split(' ')
        if len(text) != 2 or not text[-1].isdigit():
            bot.send_message(message.chat.id, 'Некорректный ввод, попробуйте еще раз /minus')
            temp_set.clear()
            return True
        if len(text) == 2 and text[-1].isdigit():
            nickname = text[-2]
            inches = int(text[-1])
            if nickname not in users:
                mess = bot.send_message(message.chat.id, f'Пользователь {nickname} еще не клубе, попробуйте еще раз')
                bot.register_next_step_handler(mess, remove)
            elif inches <= users_bonus[message.from_user.username]:
                users_bonus[message.from_user.username] -= inches
                users_scale[nickname] -= inches
                bot.send_message(message.chat.id, f'Успешно убавил пользователю <b>{nickname} {inches} см.</b>',
                                 parse_mode='html')
                resist_time = time.perf_counter()
                gayresist_d[nickname].setdefault(message.from_user.username, []).append(inches)
                temp_set.clear()
            elif inches > users_bonus[message.from_user.username]:
                bot.send_message(message.chat.id, 'У вас нет столько бонусов, попробуйте еще раз')
                temp_set.clear()
                return True
        else:
            bot.register_next_step_handler(message, remove)


# шкала сколько накинули
@bot.message_handler(commands=['scale'])
def scale(message):
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    if users_scale[message.from_user.username] > 0:
        bot.reply_to(message, f'Ваше отклонение от average равно <b>+{users_scale[message.from_user.username]} см</b>',
                     parse_mode='html')
    else:
        bot.reply_to(message, f'Ваше отклонение от average равно <b>{users_scale[message.from_user.username]} см</b>',
                     parse_mode='html')


@bot.message_handler(commands=['gayresist'])
def gayresist(message):
    # проверка на дурака
    if message.from_user.username not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    global battle_time
    # сутки не прошли
    if message.from_user.username in check_battle and check_battle[message.from_user.username] - time.perf_counter() \
            < 86400:
        bot.reply_to(message, 'баттлиться можно раз в сутки')
        del check_battle[message.from_user.username]
        return True
    elif message.from_user.username not in check_battle:
        battle_time = time.perf_counter()
        check_battle.update({message.from_user.username: battle_time})
    # сутки прошли
    elif message.from_user.username in check_battle and\
            check_battle[message.from_user.username] - time.perf_counter() >= 86400:
        del check_battle[message.from_user.username]
        battle_time = time.perf_counter()
        check_battle.update({message.from_user.username: battle_time})
    if resist_time - time.perf_counter() >= 86400:
        del gayresist_d[message.from_user.username]
        return True
    msg = 'Сегодня вам убавили:\n'
    for key, value in gayresist_d[message.from_user.username].items():
        msg += f'@{key}: <b>{sum(value)} см</b>\n'
    if message.from_user.username not in gays_time or (
            len(gays_time) != 0 and time.perf_counter() - gays_time[message.from_user.username] >= 86400):
        bot.send_message(message.chat.id, 'Кажется, нужно обновить данные, жми /gay и возвращайся')
        del check_battle[message.from_user.username]
        return True
    if msg == 'Сегодня вам убавили:\n':
        bot.send_message(message.chat.id, 'За сегодня вам никто нисколько не убавил')
        del check_battle[message.from_user.username]
        return True
    elif len(gays_time) != 0 and len(gays[message.from_user.username]) != 0 \
            and time.perf_counter() - gays_time[message.from_user.username] < 86400:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('Рискнуть', callback_data='risk')
        button2 = types.InlineKeyboardButton('Отмена', callback_data='cancel')
        markup.add(button1, button2)
        bot.reply_to(message, 'Запускаю гейрезист...')
        time.sleep(1)
        bot.send_message(message.chat.id, msg, parse_mode='html')
        time.sleep(1)
        bot.send_message(message.chat.id, f'Вероятность резиста: {gays[message.from_user.username][-1]} %',
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'risk':
            msg = bot.reply_to(call.message, 'Окей, впиши сюда ник, с кем будешь баттлиться')
            bot.register_next_step_handler(msg, battle)
        elif call.data == 'cancel':
            bot.send_message(call.message.chat.id, 'Отменил')
            return True
        elif call.data == 'hide':
            bot.delete_message(call.message.chat.id, call.message.message_id)


def battle(message):
    if message.text not in gayresist_d[message.from_user.username].keys():
        msg = bot.reply_to(message, 'Такого ника нет, попробуй еще раз')
        bot.register_next_step_handler(msg, battle)
    else:
        if random.random() < gays[message.from_user.username][-1] / 100:
            bot.send_message(message.chat.id, f'Сработало! То число, которое вам накинул {message.text},'
                                              f' отскочило от тебя и попало в него')
            users_scale[message.text] -= sum(gayresist_d[message.from_user.username][message.text])
            users_scale[message.from_user.username] += sum(gayresist_d[message.from_user.username][message.text])
        else:
            bot.send_message(message.chat.id, 'Не получилось:(\nВсе осталось по-прежнему')


# секретный дикпик
def dickpic():
    photo = open('C:/Users/Mio Welt/Documents/0.3%_chance.jpg', 'rb')
    if random.random() < 0.004:
        bot.send_message(chat_id, 'Сегодня просто ахуеть, какой счастливый день!!!!!\n'
                                  'Шанс выпадения Властелина очень, очень мал, поздравляю!!!!')
        bot.send_photo(chat_id, photo)
        return True


def do_schedule():
    schedule.every().day.at('12:00').do(dickpic)
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = Thread(target=do_schedule)
thread.start()
bot.polling(non_stop=True)
