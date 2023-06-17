import sqlite3
import telebot
import random
import time
import statistics
import schedule
from telebot import types
from threading import Thread

bot = telebot.TeleBot('')

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
id_check = {}  # gayresist
check_battle = {}
check_add = {}
check_remove = {}
chat_id = 0
resist_time = 0
summ = 0


def create_table_if_not_exists():
    conn = sqlite3.connect('dick_data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS dick_data
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT,
               scale INTEGER,
               average INTEGER,
               balance INTEGER)''')

    conn.commit()
    conn.close()


def save_to_database(username, scale, average, balance):
    conn = sqlite3.connect('dick_data.db')
    c = conn.cursor()

    c.execute("INSERT INTO dick_data (username, scale, average, balance) VALUES (?, ?, ?, ?)",
              (username, scale, average, balance))

    conn.commit()
    conn.close()


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
                          ' поэтому среднее будет 60-15=45 см. Так же, если вам кто то уменьшил за сегодняшний день, '
                          'можно попытаться стереть этот минус у себя и накинуть вдвое больше тому, кто вам накинул '
                          'через /gayresist. Если не получится, минус, который у тебя, остается. Кажется, всё.\n'
                          ' /all замеряет сразу у всех, кто прожал старт. Веселитесь!',
                 reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    global chat_id
    create_table_if_not_exists()
    if str(message.chat.id) != "-849170342":  # чтобы бот работал только в 1 чате
        return True
    name = '@' + str(message.from_user.username)
    chat_id = message.chat.id
    if message.from_user.username in users:
        bot.reply_to(message, "Ты уже в клубе", parse_mode=None)
        return True
    users.update({name: []})
    gays.update({name: []})
    users_bonus.update({name: 0})
    users_scale.update({name: 0})
    gayresist_d.update({name: {}})
    bot.send_message(message.chat.id, 'Welcome to the club, buddy!')


@bot.message_handler(commands=['measure'])
def measure(message):
    name = '@' + str(message.from_user.username)
    # проверка на дурака
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    # проверка на новую генерацию через сутки
    # если юзер существует и сутки не прошли
    if len(users_time) != 0 and len(users[name]) != 0 \
            and time.perf_counter() - users_time[name] < 86400:
        bot.reply_to(message, f'{random.choice(dicks)} сегодня'
                              f' <b>{users[name][-1]}см</b>'
                              f'{random.choice(emojis)}', parse_mode='html')
        return True
    # если новый юзер, то дать замерить либо через сутки
    elif message.from_user.username not in users_time or (
            len(users_time) != 0 and time.perf_counter() -
            users_time[name] >= 86400):

        size = random.randint(0, 200)
        users_time.update({name: time.perf_counter()})
        users[name].append(size)
        average_dicks.update({name: statistics.mean(users[name])})
        users_bonus[name] += size // 10
        bot.reply_to(message, f'{random.choice(dicks)} сегодня <b>{users[name][-1]}см</b>'
                              f'{random.choice(emojis)}', parse_mode='html')


@bot.message_handler(commands=['average'])
def average(message):
    name = '@' + str(message.from_user.username)
    # проверка на дурака
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    total = 'Усреднённые жезлы на сегодняшний день:\n'
    if len(users) != 0:
        # сортировка выводимой строки
        sorted_users = dict(reversed(sorted(average_dicks.items(), key=lambda item: item[1])))
        # упаковка строки по каждому юзеру
        for key, value in sorted_users.items():
            total += f'{str(key)}:  <b>{str(value + users_scale[key])} см</b>\n'
        bot.send_message(message.chat.id, total, parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Клуб все еще пуст, заходи /start')


# замер у всех сразу
@bot.message_handler(commands=['all'])
def all_in(message):
    name = '@' + str(message.from_user.username)
    # проверка на дурака
    if name not in users:
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
                users_bonus[name] += size // 10
                all_dict.update({user: size})
                # пополняем список пользователей
                everyone += f'{str(user)}:  <b>{str(size)} см</b>\n'

                # наоборот
            elif user in users_time and len(users[user]) != 0 and time.perf_counter() - users_time[user] < 86400:
                all_dict.update({user: users[user][-1]})
                # пополняем список пользователей
                everyone += f'{str(user)}:  <b>{str(users[user][-1])} см</b>\n'
        # вывод
        bot.send_message(message.chat.id, everyone, parse_mode='html')


# гейметр
@bot.message_handler(commands=['gay'])
def gay(message):
    name = '@' + str(message.from_user.username)
    # проверка на дурака
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True

    if len(gays_time) != 0 and len(gays[name]) != 0 \
            and time.perf_counter() - gays_time[name] < 86400:
        bot.reply_to(message, f'{name} сегодня гей на'
                              f' <b>{gays[name][-1]}%</b>', parse_mode='html')
        return True
    # если новый юзер или прошли сутки, то дать замерить
    elif name not in gays_time or (
            len(gays_time) != 0 and time.perf_counter() - gays_time[name] >= 86400):

        size = random.randint(0, 100)
        gays_time.update({name: time.perf_counter()})
        gays[name].append(size)
        bot.reply_to(message, f'{name} сегодня гей на'
                              f' <b>{gays[name][-1]}%</b>', parse_mode='html')


# средние геи
@bot.message_handler(commands=['gayaverage'])
def gayaverage(message):
    name = '@' + str(message.from_user.username)
    # проверка на дурака
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True

    total = 'Посмотрим на латентных наших средних:\n'
    if len(gays) != 0:
        # сортировка выводимой строки
        sorted_gays = dict(reversed(sorted(gays.items(), key=lambda item: item[1])))
        # упаковка строки по каждому юзеру
        for key, value in sorted_gays.items():
            total += f'{str(key)}: <b>{str(statistics.mean(value))} %</b>\n'
        bot.send_message(message.chat.id, total, parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Клуб все еще пуст, заходи /start')


# проверка баланса
@bot.message_handler(commands=['balance'])
def balance(message):
    name = '@' + str(message.from_user.username)
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    bot.reply_to(message, f'Ваш текущий баланс: <b>{users_bonus[name]} очков</b>',
                 parse_mode='html')


# прибавить кому-то см к среднему
@bot.message_handler(commands=['plus'])
def plus(message):
    name = '@' + str(message.from_user.username)
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    if len(temp_set) != 0:
        msg = bot.send_message(message.chat.id, f'Подожди, пока {temp_set[0]} завершит операцию')
        bot.register_next_step_handler(msg, add)
    else:
        temp_set.append(name)
        msg1 = bot.send_message(message.chat.id, 'Введите ник и число через пробел - кому и сколько хотите накинуть.'
                                                 '(@Jimmythedoc 10)\n'
                                                 'Для отмены нажмите /cancel')
        bot.register_next_step_handler(msg1, add)


def add(message):
    name = '@' + str(message.from_user.username)
    if name in temp_set and (message.text == '/cancel' or message.text == '/cancel@Mr_dick_bot'):
        bot.reply_to(message, 'Галя, отмена!')
        temp_set.clear()
        return True
    elif name in temp_set and message.text != '/cancel' and message.text != '/cancel@Mr_dick_bot':
        text = message.text.split(' ')
        if len(text) != 2 or not text[-1].isdigit():
            bot.send_message(message.chat.id, 'Некорректный ввод, попробуйте еще раз /plus')
            temp_set.clear()
            return True
        if len(text) == 2 and text[-1].isdigit():
            # проверка на сутки этого пользователя
            if name not in check_add:
                check_add.update({name: {message.text[-2]: 0}})
                if check_add[name][message.text[-2]] - time.perf_counter() >= 86400 or \
                        check_add[name][message.text[-2]] == 0:
                    nickname = text[-2]
                    inches = int(text[-1])
                    if nickname not in users_bonus:
                        mess0 = bot.send_message(message.chat.id, f'Пользователь {nickname} еще не клубе,'
                                                                  f' попробуйте еще раз')
                        bot.register_next_step_handler(mess0, add)
                    elif inches <= users_bonus[name]:
                        users_bonus[name] -= inches
                        users_scale[nickname] += inches
                        bot.send_message(message.chat.id, f'Успешно накинул пользователю {nickname} '
                                                          f'<b>{inches} см.</b>',
                                         parse_mode='html')
                        gayresist_d[nickname].setdefault(name, []).append(int(inches))
                        battle_time = time.perf_counter()
                        check_add.update({name: {message.text[-2]: battle_time}})
                        temp_set.clear()
                    elif inches > users_bonus[name]:
                        bot.send_message(message.chat.id, 'У вас нет столько бонусов, попробуйте заново /plus')
                        temp_set.clear()
                        return True
            else:
                if message.text[-2] in check_add[name].keys():
                    if check_add[name][message.text[-2]] - time.perf_counter() >= 86400:
                        battle_time = time.perf_counter()
                        check_add.update({name: {message.text[-2]: battle_time}})
                        nickname = text[-2]
                        inches = int(text[-1])
                        if nickname not in users_bonus:
                            mess0 = bot.send_message(message.chat.id,
                                                     f'Пользователь {nickname} еще не клубе, попробуйте еще раз')
                            bot.register_next_step_handler(mess0, add)
                        elif inches <= users_bonus[name]:
                            users_bonus[name] -= inches
                            users_scale[nickname] += inches
                            bot.send_message(message.chat.id,
                                             f'Успешно накинул пользователю {nickname} <b>{inches} см.</b>',
                                             parse_mode='html')
                            gayresist_d[nickname].setdefault(name, []).append(int(inches))
                            temp_set.clear()
                        elif inches > users_bonus[name]:
                            bot.send_message(message.chat.id, 'У вас нет столько бонусов, попробуйте заново /plus')
                            temp_set.clear()
                            return True
                    else:
                        bot.reply_to(message, 'Сегодня ты уже ему накинул')
                        temp_set.clear()
                        return True
                else:
                    battle_time = time.perf_counter()
                    check_add.update({name: {message.text[-2]: battle_time}})
                    nickname = text[-2]
                    inches = int(text[-1])
                    if nickname not in users_bonus:
                        mess0 = bot.send_message(message.chat.id,
                                                 f'Пользователь {nickname} еще не клубе, попробуйте еще раз')
                        bot.register_next_step_handler(mess0, add)
                    elif inches <= users_bonus[name]:
                        users_bonus[name] -= inches
                        users_scale[nickname] += inches
                        bot.send_message(message.chat.id,
                                         f'Успешно накинул пользователю {nickname} <b>{inches} см.</b>',
                                         parse_mode='html')
                        gayresist_d[nickname].setdefault(name, []).append(int(inches))
                        temp_set.clear()
                    elif inches > users_bonus[name]:
                        bot.send_message(message.chat.id, 'У вас нет столько бонусов, попробуйте заново /plus')
                        temp_set.clear()
                        return True
    elif name not in temp_set:
        bot.register_next_step_handler(message, add)


# отнять у кого-то см от среднего
@bot.message_handler(commands=['minus'])
def minus(message):
    name = '@' + str(message.from_user.username)
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    if len(temp_set) != 0:
        msg = bot.send_message(message.chat.id, f'Подожди, пока {temp_set[0]} завершит операцию')
        bot.register_next_step_handler(msg, remove)
    if name in users:
        temp_set.append(name)
        message1 = bot.reply_to(message, 'Введите ник и число через пробел - кому и сколько хотите убавить.'
                                         '(@Jimmythedoc 10)\n'
                                         'Для отмены нажмите /cancel')
        bot.register_next_step_handler(message1, remove)


def remove(message):
    global resist_time
    name = '@' + str(message.from_user.username)
    if name in temp_set and (message.text == '/cancel' or message.text == '/cancel@Mr_dick_bot'):
        bot.reply_to(message, 'Галя, отмена!')
        temp_set.clear()
        return True
    elif name in temp_set and message.text != '/cancel' and message.text != '/cancel@Mr_dick_bot':
        text = message.text.split(' ')
        if len(text) != 2 or not text[-1].isdigit():
            bot.send_message(message.chat.id, 'Некорректный ввод, попробуйте еще раз /minus')
            temp_set.clear()
            return True
        if len(text) == 2 and text[-1].isdigit():
            # проверка на сутки этого пользователя
            if name not in check_remove:
                check_remove.update({name: {message.text[-2]: 0}})
                if check_remove[name][message.text[-2]] - time.perf_counter() >= 86400 or \
                        check_remove[name][message.text[-2]] == 0:
                    nickname = text[-2]
                    inches = int(text[-1])
                    if nickname not in users:
                        mess = bot.send_message(message.chat.id, f'Пользователь {nickname} еще не клубе,'
                                                                 f' попробуйте еще раз')
                        bot.register_next_step_handler(mess, remove)
                    elif inches <= users_bonus[name]:
                        users_bonus[name] -= inches
                        users_scale[nickname] -= inches
                        bot.send_message(message.chat.id, f'Успешно убавил пользователю {nickname} <b>{inches} см.</b>',
                                         parse_mode='html')
                        resist_time = time.perf_counter()
                        gayresist_d[nickname].setdefault(name, []).append(int('-' + str(inches)))
                        temp_set.clear()
                    elif inches > users_bonus[name]:
                        bot.send_message(message.chat.id, 'У вас нет столько бонусов, попробуйте еще раз /minus')
                        temp_set.clear()
                        return True
            else:
                if message.text[-2] in check_remove[name].keys():
                    if check_remove[name][message.text[-2]] - time.perf_counter() >= 86400:
                        battle_time = time.perf_counter()
                        check_remove.update({name: {message.text[-2]: battle_time}})
                        nickname = text[-2]
                        inches = int(text[-1])
                        if nickname not in users:
                            mess = bot.send_message(message.chat.id,
                                                    f'Пользователь {nickname} еще не клубе, попробуйте еще раз')
                            bot.register_next_step_handler(mess, remove)
                        elif inches <= users_bonus[name]:
                            users_bonus[name] -= inches
                            users_scale[nickname] -= inches
                            bot.send_message(message.chat.id,
                                             f'Успешно убавил пользователю {nickname} <b>{inches} см.</b>',
                                             parse_mode='html')
                            resist_time = time.perf_counter()
                            gayresist_d[nickname].setdefault(name, []).append(int('-' + str(inches)))
                            temp_set.clear()
                        elif inches > users_bonus[name]:
                            bot.send_message(message.chat.id, 'У вас нет столько бонусов, попробуйте еще раз /minus')
                            temp_set.clear()
                            return True
                    else:
                        bot.reply_to(message, 'Сегодня ты уже ему убавил')
                        temp_set.clear()
                        return True
                else:
                    battle_time = time.perf_counter()
                    check_remove.update({name: {message.text[-2]: battle_time}})
                    nickname = text[-2]
                    inches = int(text[-1])
                    if nickname not in users:
                        mess = bot.send_message(message.chat.id,
                                                f'Пользователь {nickname} еще не клубе, попробуйте еще раз')
                        bot.register_next_step_handler(mess, remove)
                    elif inches <= users_bonus[name]:
                        users_bonus[name] -= inches
                        users_scale[nickname] -= inches
                        bot.send_message(message.chat.id, f'Успешно убавил пользователю {nickname} <b>{inches} см.</b>',
                                         parse_mode='html')
                        resist_time = time.perf_counter()
                        gayresist_d[nickname].setdefault(name, []).append(int('-' + str(inches)))
                        temp_set.clear()
                    elif inches > users_bonus[name]:
                        bot.send_message(message.chat.id, 'У вас нет столько бонусов, попробуйте еще раз /minus')
                        temp_set.clear()
                        return True
    elif name not in temp_set:
        bot.register_next_step_handler(message, remove)


# шкала сколько накинули
@bot.message_handler(commands=['scale'])
def scale(message):
    name = '@' + str(message.from_user.username)
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    if users_scale[name] > 0:
        bot.reply_to(message, f'Ваше отклонение от average равно <b>+{users_scale[name]} см</b>',
                     parse_mode='html')
    else:
        bot.reply_to(message, f'Ваше отклонение от average равно <b>{users_scale[name]} см</b>',
                     parse_mode='html')


@bot.message_handler(commands=['gayresist'])
def gayresist(message):
    name = '@' + str(message.from_user.username)
    # проверка на дурака
    if name not in users:
        bot.send_message(message.chat.id, 'Ты пока не в клубе, жми /start')
        return True
    global summ
    # чистка словаря 'сегодня вам накинул'
    if resist_time - time.perf_counter() >= 86400:
        del gayresist_d[name]
        return True
    msg = 'Сегодня вам убавили:\n'
    for key, value in gayresist_d[name].items():
        msg += f'{key}: <b>{sum(value)} см</b>\n'
        summ = sum(value)
    if msg == 'Сегодня вам убавили:\n':
        bot.send_message(message.chat.id, 'За сегодня вам никто нисколько не убавил')
        return True
    elif name not in gays_time or (len(gays_time) != 0 and time.perf_counter() - gays_time[name] >= 86400):
        bot.send_message(message.chat.id, 'Кажется, нужно обновить данные, жми /gay и возвращайся')
        return True
    elif len(gays_time) != 0 and len(gays[name]) != 0 and time.perf_counter() - gays_time[name] < 86400 and summ < 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('Рискнуть', callback_data='risk')
        button2 = types.InlineKeyboardButton('Отмена', callback_data='cancel')
        markup.add(button1, button2)
        bot.reply_to(message, 'Запускаю гейрезист...')
        time.sleep(1)
        bot.send_message(message.chat.id, msg, parse_mode='html')
        time.sleep(1)
        send_message = bot.send_message(message.chat.id, f'Вероятность резиста: {gays[name][-1]} %',
                                        reply_markup=markup)
        id_check.update({message.from_user.id: send_message.message_id})
    elif len(gays_time) != 0 and len(gays[name]) != 0 and time.perf_counter() - gays_time[name] < 86400 and summ >= 0:
        bot.reply_to(message, 'В минус тебе сегодня никто не накинул')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'risk':
        if id_check.get(call.from_user.id, 0) != call.message.message_id:
            return True
        msg = bot.reply_to(call.message, 'Окей, впиши сюда ник, с кем будешь баттлиться(@Jimmythedoc)')
        bot.register_next_step_handler(msg, battle)
    elif call.data == 'cancel' and id_check.get(call.from_user.id, 0) == call.message.message_id:
        bot.send_message(call.message.chat.id, 'Отменил')
        return True
    elif call.data == 'hide':
        bot.delete_message(call.message.chat.id, call.message.message_id)


def battle(message):
    name = '@' + str(message.from_user.username)
    if message.text in gayresist_d[name]:
        if name not in check_battle:
            check_battle.update({name: {message.text: 0}})
            if check_battle[name][message.text] - time.perf_counter() >= 86400 or \
                    check_battle[name][message.text] == 0:
                if random.random() < gays[name][-1] / 100:
                    bot.send_message(message.chat.id, f'Сработало! То число, которое вам накинул {message.text},'
                                                      f' отскочило от тебя и попало в него в размере х2')
                    users_scale[message.text] += 2 * sum(gayresist_d[name][message.text])
                    users_scale[name] -= sum(gayresist_d[name][message.text])
                    battle_time = time.perf_counter()
                    check_battle.update({name: {message.text: battle_time}})
                else:
                    bot.send_message(message.chat.id, 'Не получилось:(\nЭтот минус вам удвоился')
                    users_scale[name] += sum(gayresist_d[name][message.text])
        else:
            if message.text in check_battle[name].keys():
                if check_battle[name][message.text] - time.perf_counter() >= 86400:
                    battle_time = time.perf_counter()
                    check_battle.update({name: {message.text: battle_time}})
                else:
                    bot.reply_to(message, 'Сегодня ты уже с ним баттлился')
            else:
                battle_time = time.perf_counter()
                check_battle.update({name: {message.text: battle_time}})
            if message.text not in gayresist_d[name].keys():
                msg = bot.reply_to(message, 'Такого ника нет, попробуй еще раз')
                bot.register_next_step_handler(msg, battle)
            elif message.text in gayresist_d[name].keys() and \
                    ((message.text in check_battle[name].keys() and
                      check_battle[name][message.text] - time.perf_counter() >= 86400) or
                     (message.text not in check_battle[name].keys())):
                if random.random() < gays[name][-1] / 100:
                    bot.send_message(message.chat.id, f'Сработало! То число, которое вам накинул {message.text},'
                                                      f' отскочило от тебя и попало в него в размере х2 ')
                    users_scale[message.text] += 2 * sum(gayresist_d[name][message.text])
                    users_scale[name] -= sum(gayresist_d[name][message.text])
                else:
                    bot.send_message(message.chat.id, 'Не получилось:(\nЭтот минус вам удвоился')
                    users_scale[name] += sum(gayresist_d[name][message.text])
    else:
        msg = bot.reply_to(message, 'Он тебе сегодня не убавлял, попробуй другой ник')
        bot.register_next_step_handler(msg, battle)


# секретный дикпик
def dickpic():
    photo = open('C:/Users/Mio Welt/Documents/0.3%_chance.jpg', 'rb')
    if random.random() < 0.004:
        bot.send_photo(chat_id, photo)
        return True


def do_schedule():
    schedule.every().day.at('12:00').do(dickpic)
    while True:
        for username in users:
            if average_dicks:
                schedule.every(30).seconds.do(save_to_database, username, users_scale[username],
                                              average_dicks[username], users_bonus[username])
            else:
                schedule.every(30).seconds.do(save_to_database, username, users_scale[username],
                                              0, users_bonus[username])
        schedule.run_pending()
        time.sleep(1)

thread = Thread(target=do_schedule)
thread.start()
bot.polling(non_stop=True)
