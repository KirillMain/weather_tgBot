import time
import ast
import telebot
import config
import weather
import schedule
from threading import Thread
import image

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open("tgweatherBOT/data/chooses/users_params.txt", "r", encoding="utf-8") as f:
        d = ast.literal_eval(f.read())
        idd = str(message.from_user.id)
        if idd not in d.keys():
            d.update({idd: ['Облачность', 'Давление', 'Индекс УФ', 'Влажность', 'Ветер']})
    with open("tgweatherBOT/data/chooses/users_params.txt", "w", encoding="utf-8") as f:
        f.write(str(d))
    st = open("tgweatherBOT/stick/hello.tgs", 'rb')
    bot.send_sticker(message.chat.id, st)

    text = f'Привет, {message.from_user.first_name},\n' \
           f'Я могу высылать тебе погоду на сегодня и неделю вперед!\n' \
           f'Напиши /help или нажми на "Инфо" для большей информации.'
    btns_main(message, text)


@bot.message_handler(commands=['help'])
def send_help(message):
    text = 'Я умею высылать погоду на сегодня и неделю вперед!\n\n' \
           '"Настройки" - тут ты можешь выбрать какие характеристики погоды мне высылать.\n' \
           '"Рассылка" - тут ты можешь подписаться на ежедневную рассылку.\n'
    btns_main(message, text)


@bot.message_handler()
def common_message(message):
    if message.text == 'лева лох ебаный':
        text = 'Полностью согласен, а еще он хуесос, у меня есть докозательства'
        btns_main(message, text)
        
    elif message.text in '1234567891011121314':
        text = month_text(message)
        btns_main(message, text)

    elif message.text == "Сегодня☀️":
        text = today(message)
        btns_main(message, text)

    elif message.text == "Неделя⛅️":
        boolean = check_for_text(message)
        if boolean:
            text = 'Выбери на какое количество дней ты хочешь узнать погоду.\n\nТакже можно написать число (до 14).'
            btns_select_days(message, text)
        else:
            text = month(message)
            btns_main(message, text)

    elif message.text == "Рассылка📪":
        text = "Выберите, во сколько будет присылаться прогноз погоды.\n" \
               "Например: 10:00, 08:00 и т.д\n" \
               "!!минуты всегда :00!!"

        with open('tgweatherBOT/data/chooses/user_times.txt', 'r', encoding='utf-8') as f:
            d = ast.literal_eval(f.read())
            idd = message.from_user.id
            text_user_times = ''
            for k in d.keys():
                if idd in d[k]:
                    if text_user_times != '':
                        text_user_times += ", "
                    text_user_times += f"{k}"
            text += f'\n\nСейчас рассылка в {text_user_times}.'
        btns_select_times(message, text)

    elif message.text[0] == "И" and message.text[1] == 'н':
        send_help(message)

    elif message.text[0] == "Н" and message.text[2] == "с":
        with open("tgweatherBOT/data/chooses/users_params.txt", "r", encoding="utf-8") as f:
            dic = ast.literal_eval(f.read())
            idd = str(message.from_user.id)
            arr = dic[idd]
            if 'Текст' in arr:
                t = 'формат: текст'
            else:
                t = 'формат: фото'
            text = f"Выберите какие характеристики погоды будут высылаться ({t})."

        if len(arr) != 0 or arr == ['Текст']:
            text += f'\n\nСейчас у тебя будут показываться следующие характеристики:\n'
            for i in arr:
                if i != arr[0]:
                    text += f", "
                text += f'{i}'
        else:
            text += "\n\nСейчас у Вас выводится лишь температура."
        btns_choose_today(message, text)

    elif message.text[:-1] == "Облачность":
        text = check_parametrs(message)
        btns_choose_today(message, text)

    elif message.text[:-1] == "Давление":
        text = check_parametrs(message)
        btns_choose_today(message, text)

    elif message.text[:-1] == "Индекс УФ":
        text = check_parametrs(message)
        btns_choose_today(message, text)

    elif message.text[:-1] == "Влажность":
        text = check_parametrs(message)
        btns_choose_today(message, text)

    elif message.text[:-1] == "Ветер":
        text = check_parametrs(message)
        btns_choose_today(message, text)

    elif message.text[:-1] == "Текст":
        text = check_parametrs(message)
        btns_choose_today(message, text)

    elif message.text == "Назад":
        text = "Вы вернулись в главное меню."
        btns_main(message, text)

    elif message.text in {'00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                          '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                          '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                          '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'}:
        text = times(message)
        btns_main(message, text)

    else:
        text = "Чо???"
        btns_main(message, text)


def on_click(message):
    common_message(message)


def btns_main(message, text):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Сегодня☀️")
    btn2 = telebot.types.KeyboardButton("Неделя⛅️")
    markup.row(btn1, btn2)

    btn3 = telebot.types.KeyboardButton("Рассылка📪")
    btn4 = telebot.types.KeyboardButton("Инфоℹ️️")
    btn5 = telebot.types.KeyboardButton("Настройки⚙️️")
    markup.row(btn3, btn4, btn5)

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def btns_choose_today_xar(dic, xar):
    if xar in dic:
        t = telebot.types.KeyboardButton(f'{xar}✅')
    else:
        t = telebot.types.KeyboardButton(f'{xar}❌')
    return t


def btns_choose_today(message, text):
    with open("tgweatherBOT/data/chooses/users_params.txt", "r", encoding="utf-8") as f:
        asd = ast.literal_eval(f.read())
        idd = str(message.from_user.id)
        if idd not in asd.keys():
            asd.update({idd: []})
        dic = asd[idd]
    with open("tgweatherBOT/data/chooses/users_params.txt", "w", encoding="utf-8") as f:
        f.write(str(asd))

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = btns_choose_today_xar(dic, "Облачность")
    btn2 = btns_choose_today_xar(dic, "Давление")
    btn3 = btns_choose_today_xar(dic, "Индекс УФ")
    markup.row(btn1, btn2, btn3)

    btn4 = btns_choose_today_xar(dic, "Влажность")
    btn5 = btns_choose_today_xar(dic, "Ветер")
    btn6 = btns_choose_today_xar(dic, "Текст")
    btn7 = telebot.types.KeyboardButton("Назад")
    markup.row(btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def check_parametrs(message):
    with open("tgweatherBOT/data/chooses/users_params.txt", "r", encoding="utf-8") as f:
        dic = ast.literal_eval(f.read())
        idd = str(message.from_user.id)
        if message.text[:-1] in dic[idd]:
            boolean = True
        else:
            boolean = False

    with open("tgweatherBOT/data/chooses/users_params.txt", "w", encoding="utf-8") as f:
        arr = dic[idd]
        if boolean:
            if message.text[:-1] == "Текст":
                text = f"Теперь вам будет высылать погода в картинке!"
            else:
                text = f"{message.text[:-1]} был(а) удален(а) из списка."
            arr.remove(message.text[:-1])
            dic.update({idd: arr})
        else:
            if message.text[:-1] == "Текст":
                text = f"Теперь вам будет высылать погода в виде текстового сообщения!"
            else:
                text = f"{message.text[:-1]} был(а) добавлен(а) в список."
            arr.append(message.text[:-1])
            dic.update({idd: arr})

        f.write(str(dic))

    if len(arr) != 0:
        text += f'\n\nСейчас у Вас будут показываться следующие характеристики:\n'
        for i in arr:
            if i != arr[0]:
                text += f", "
            text += f'{i}'
    else:
        text += "\n\nСейчас у Вас выводится лишь температура."
    return text


def btns_select_days(message, text):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("1")
    btn2 = telebot.types.KeyboardButton("2")
    btn3 = telebot.types.KeyboardButton("3")
    btn4 = telebot.types.KeyboardButton("4")
    btn5 = telebot.types.KeyboardButton("5")
    btn6 = telebot.types.KeyboardButton("6")
    markup.row(btn1, btn2, btn3, btn4, btn5, btn6)

    btn7 = telebot.types.KeyboardButton("7")
    btnback = telebot.types.KeyboardButton('Назад')
    markup.row(btn7, btnback)

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def btns_select_times(message, text):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton("Назад")
    markup.row(btn1)

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def times(message):
    with open('tgweatherBOT/data/chooses/user_times.txt', 'r', encoding='utf-8') as f:
        d = ast.literal_eval(f.read())

    timee = message.text
    idd = message.from_user.id
    arr = d[timee]
    if idd not in arr:
        arr.append(idd)
        text = f"Время {timee} было добавлено в рассылку."
    else:
        arr.remove(idd)
        text = f"Время {timee} было убрано из рассылки."

    with open('tgweatherBOT/data/chooses/user_times.txt', 'w', encoding='utf-8') as f:
        f.write(str(d))

    text_user_times = ''
    for k in d.keys():
        if idd in d[k]:
            if text_user_times != '':
                text_user_times += ", "
            text_user_times += f"{k}"

    text += f"\nТеперь Вам будет ежедневно в {text_user_times} высылаться погода на день."
    return text


def check_for_text(message):
    with open("tgweatherBOT/data/chooses/users_params.txt", 'r', encoding='utf-8') as f:
        dic = ast.literal_eval(f.read())
        idd = str(message.from_user.id)
        arr = dic[str(idd)]

        if 'Текст' in dic[str(idd)]:
            return True
        else:
            return False


def month(message):
    with open("tgweatherBOT/data/chooses/users_params.txt", 'r', encoding='utf-8') as f:
        dic = ast.literal_eval(f.read())
        idd = str(message.from_user.id)
        arr = dic[str(idd)]

        if 'Текст' in dic[idd]:
            text = month_text(message)
        else:
            text = image.month(arr)
            bot.send_photo(idd, open('data/hz/res_month.png', 'rb'))
    return text


def month_text(message):
    try:
        asd = int(message.text)

        with open("tgweatherBOT/data/chooses/users_params.txt", 'r', encoding='utf-8') as f:
            dic = ast.literal_eval(f.read())
            idd = str(message.from_user.id)
            arr = dic[idd]

        d = weather.w_month()

        text = ""
        if asd <= 0 or asd > 14:
            text = "Не ну ты еблан я хуею."
        else:
            for i in range(asd):
                if i != 0:
                    text += '\n'
                text += f"------------{d['arr_days'][i]}------------\n" \
                        f"Температура: {d['arr_temp'][i]}"

                if "Облачность" in arr:
                    text += f'\nОблачность: {d["arr_sost"][i]}'
                if "Давление" in arr:
                    text += f'\nДавление: {d["arr_davl"][i]}'
                if "Индекс УФ" in arr:
                    text += f'\nИндекс УФ: {d["arr_yf"][i]}'
                if "Влажность" in arr:
                    text += f'\nВлажность: {d["arr_vlag"][i]}'
                if "Ветер" in arr:
                    text += f'\nВетер: {d["arr_wind"][i]}'

    except ValueError:
        text = "Ты чо мне пишешь? Числа ебень, валенок."

    return text


def today(message, check=False):  # check - рассылка или нет
    with open("data/chooses/users_params.txt", 'r', encoding='utf-8') as f:
        dic = ast.literal_eval(f.read())
        if not check:
            idd = str(message.from_user.id)
        else:
            idd = str(message)
        arr = dic[str(idd)]

        if 'Текст' in dic[idd]:
            text = today_text(message, arr, idd)
        else:
            text = image.today(message, arr, idd)
            bot.send_photo(idd, open('data/hz/res_today.png', 'rb'))
    return text


def today_text(message, arr, idd):
    d = weather.w_today()

    leng = len(d['arr_time'])

    t = 0
    for i in range(leng):
        if d["arr_time"][i] == "00:00":
            break
        x = d['arr_temp'][i][:-1]
        if x[0] == "+":
            t += int(x[1:])
        else:
            t -= int(x[1:])
    t /= leng
    if t > 30:
        st = open("stick/zharko.tgs", 'rb')
        bot.send_sticker(idd, st)
    elif t > 20:
        st = open("stick/sunny.tgs", 'rb')
        bot.send_sticker(idd, st)
    elif t > 10:
        st = open("stick/norm.tgs", 'rb')
        bot.send_sticker(idd, st)
    elif t < -10:
        st = open("stick/xolod.webm", 'rb')
        bot.send_sticker(idd, st)

    text = ""
    for i in range(leng):
        if i != 0:
            text += '\n'
        if d["arr_time"][i] == "00:00":
            break

        text += f'----------Время: {d["arr_time"][i]}----------\n' \
                f'Температура: {d["arr_temp"][i]}'

        if "Облачность" in arr:
            text += f'\nОблачность: {d["arr_sost"][i]}'
        if "Давление" in arr:
            text += f'\nДавление: {d["arr_davl"][i]}'
        if "Индекс УФ" in arr:
            text += f'\nИндекс УФ: {d["arr_yf"][i]}'
        if "Влажность" in arr:
            text += f'\nВлажность: {d["arr_vlag"][i]}'
        if "Ветер" in arr:
            text += f'\nВетер: {d["arr_wind"][i]}'

    return text


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def mailing():
    weather.w_today(True)
    weather.w_info_today(True)
    weather.w_month(True)
    with open('data/chooses/user_times.txt', 'r', encoding='utf-8') as f:
        d = ast.literal_eval(f.read())

    timee = time.ctime(time.time()).split()
    now_hours = timee[3].split(":")[0]

    if len(now_hours) == 1:
        timee = f"0{now_hours}:00"
    else:
        timee = f"{now_hours}:00"

    for idd in d[timee]:
        text = today(idd, check=True)
        bot.send_message(idd, text)


if __name__ == "__main__":
    schedule.every().day.at("00:00:00").do(mailing)
    schedule.every().day.at("01:00:00").do(mailing)
    schedule.every().day.at("02:00:00").do(mailing)
    schedule.every().day.at("03:00:00").do(mailing)
    schedule.every().day.at("04:00:00").do(mailing)
    schedule.every().day.at("05:00:00").do(mailing)
    schedule.every().day.at("06:00:00").do(mailing)
    schedule.every().day.at("07:00:00").do(mailing)
    schedule.every().day.at("08:00:00").do(mailing)
    schedule.every().day.at("09:00:00").do(mailing)
    schedule.every().day.at("10:00:00").do(mailing)
    schedule.every().day.at("11:00:00").do(mailing)
    schedule.every().day.at("12:00:00").do(mailing)
    schedule.every().day.at("13:00:00").do(mailing)
    schedule.every().day.at("14:00:00").do(mailing)
    schedule.every().day.at("15:00:00").do(mailing)
    schedule.every().day.at("16:00:00").do(mailing)
    schedule.every().day.at("17:00:00").do(mailing)
    schedule.every().day.at("18:00:00").do(mailing)
    schedule.every().day.at("19:00:00").do(mailing)
    schedule.every().day.at("20:00:00").do(mailing)
    schedule.every().day.at("21:00:00").do(mailing)
    schedule.every().day.at("22:00:00").do(mailing)
    schedule.every().day.at("23:00:00").do(mailing)

    # Раскрутите поток, чтобы запустить проверку расписания, чтобы он не блокировал вашего бота.
    # Для этого потребуется функция schedule_checker, которая будет проверять каждую секунду
    # to see if the scheduled job needs to be ran.
    Thread(target=schedule_checker).start()

bot.polling(none_stop=True, interval=0)
