import weather
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
# iconixar


def popa_today(sost='cloudy'):

    fronteground = Image.open(f"data/hz/icons/icon_{sost}.png")
    back = Image.open("data/hz/main1.png")
    crop = fronteground.resize(size=(200, 200))

    back.paste(crop, (50, 100), crop)

    back.save("data/hz/prebuild_today_png.png")


def today(message, arr, idd):
    dic = weather.w_today()
    lis = weather.w_info_today()

    if 'дождь' in lis[1]:
        popa_today("rain")
    elif "облачно" in lis[1]:
        popa_today('cloudy')
    elif "ясно" in lis[1]:
        popa_today('sunny')
    elif "гроза" in lis[1]:
        popa_today('storm')
    elif "снег" in lis[1] or "метель" in lis[1]:
        popa_today('snowfall')
    elif "qwe" in lis[1]:
        ...
    elif "qwe" in lis[1]:
        ...
    else:
        popa_today()

    img = Image.open('data/hz/prebuild_today_png.png')
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 50)
    draw.text((50, 50), lis[0], (255, 255, 255), font=font)

    font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 30)
    draw.text((600, 150), lis[2], (255, 255, 255), font=font)
    draw.text((600, 190), lis[3], (255, 255, 255), font=font)
    draw.text((600, 230), lis[4], (255, 255, 255), font=font)

    font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 150)
    draw.text((280, 150), lis[1], (255, 255, 255), font=font)

    for k in range(70, 1920, 450):
        font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 40)
        if k != 1870:
            draw.text((k, 300), '-------------------------   ', (255, 255, 255), font=font)
            draw.text((k, 370), '-------------------------   ', (255, 255, 255), font=font)

            draw.text((k, 670), '-------------------------   ', (255, 255, 255), font=font)
            draw.text((k, 740), '-------------------------   ', (255, 255, 255), font=font)
            draw.text((k, 1045), '-------------------------   ', (255, 255, 255), font=font)

        font = ImageFont.truetype('data/intelone-mono-font-family-regular.otf', size=40)
        draw.text((k - 25, 300), '|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|', (255, 255, 255), font=font)

    x = 150
    for i in range(0, 24, 3):
        y = 330

        font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 50)
        draw.text((x + 80 + i*150, y), dic['arr_time'][i], (255, 255, 255), font=font)
        if i >= 12:
            draw.text((x + 80 + (i-12) * 150, 700), dic['arr_time'][i], (255, 255, 255), font=font)

        font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 30)
        draw.text((x + i * 150, 420), dic['arr_temp'][i], (255, 255, 255), font=font)
        if i >= 12:
            draw.text((x + (i - 12) * 150, 790), dic['arr_temp'][i], (255, 255, 255), font=font)

        y = 0
        if "Облачность" in arr:
            t = dic['arr_sost'][i]
            if ',' in t:
                t = t.split(',')[0]
            if t == 'Переменная облачность':
                t = "Облачно"
            draw.text((x + i * 150, 460 + y), t, (255, 255, 255), font=font)
            if i >= 12:
                draw.text((x + (i - 12) * 150, 830 + y), t, (255, 255, 255), font=font)
            y += 40

        if "Давление" in arr:
            draw.text((x + i * 150, 460 + y), dic['arr_davl'][i], (255, 255, 255), font=font)
            if i >= 12:
                draw.text((x + (i - 12) * 150, 830 + y), dic['arr_davl'][i], (255, 255, 255), font=font)
            y += 40

        if "Индекс УФ" in arr:
            draw.text((x + i * 150, 460 + y), "УФ: " + dic['arr_yf'][i], (255, 255, 255), font=font)
            if i >= 12:
                draw.text((x + (i - 12) * 150, 830 + y), "УФ: " + dic['arr_yf'][i], (255, 255, 255), font=font)
            y += 40

        if "Влажность" in arr:
            draw.text((x + i * 150, 460 + y), dic['arr_vlag'][i], (255, 255, 255), font=font)
            if i >= 12:
                draw.text((x + (i - 12) * 150, 830 + y), dic['arr_vlag'][i], (255, 255, 255), font=font)
            y += 40

        if "Ветер" in arr:
            draw.text((x + i * 150, 460 + y), dic['arr_wind'][i], (255, 255, 255), font=font)
            if i >= 12:
                draw.text((x + (i - 12) * 150, 830 + y), dic['arr_wind'][i], (255, 255, 255), font=font)
            y += 40

    img.save("data/hz/res_today.png")

    text = "Картинка😵‍💫"
    return text
# today(1, ['Влажность', 'Облачность', 'Давление', 'Индекс УФ', 'Ветер'] , '1691943259')


def popa_month(lis):
    back = Image.open("tgweatherBOT/data/hz/main1.png")

    for i in range(0, 7):
        sost = 'cloudy'

        if 'дождь' in lis[i]:
            sost = "rain"
        elif "облачно" in lis[i]:
            sost = 'cloudy'
        elif "ясно" in lis[i]:
            sost = 'sunny'
        elif "гроза" in lis[i]:
            sost = 'storm'
        elif "снег" in lis[1] or "метель" in lis[i]:
            sost = 'snowfall'
        elif "qwe" in lis[i]:
            ...
        elif "qwe" in lis[i]:
            ...

        fronteground = Image.open(f"tgweatherBOT/data/hz/icons/icon_{sost}.png")

        k = 0
        if i == 0:
            k = 150
        crop = fronteground.resize(size=(150 + k, 150 + k))

        if i == 0:
            x = -45
            y = -15
        else:
            x = (i - 1) * 300 + 30
            y = 390
        back.paste(crop, (95 + x, 50 + y), crop)

    back.save("data/hz/prebuild_month_png.png")


def month(arr):
    dic = weather.w_month()
    lis = dic['arr_sost']
    days = dic['arr_days']
    temp = dic['arr_temp']
    sost = dic['arr_sost']
    davl = dic['arr_davl']
    yf = dic['arr_yf']
    vlag = dic['arr_vlag']
    wind = dic['arr_wind']

    popa_month(lis)

    img = Image.open('data/hz/prebuild_month_png.png')
    draw = ImageDraw.Draw(img)

    for k in range(60, 1861, 300):
        font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 40)
        if k != 1860:
            draw.text((k, 335), '----------------   ', (255, 255, 255), font=font)
            draw.text((k, 400), '----------------   ', (255, 255, 255), font=font)

            draw.text((k, 995), '----------------   ', (255, 255, 255), font=font)

        font = ImageFont.truetype('data\intelone-mono-font-family-regular.otf', size=40)
        draw.text((k - 25, 340), '|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|', (255, 255, 255), font=font)

    font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 70)
    draw.text((380, 50), "Сегодня, " + days[0], (255, 255, 255), font=font)

    font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 40)
    x = 380
    y = 130
    draw.text((x, y), temp[0], (255, 255, 255), font=font)
    y += 70

    if "Облачность" in arr:
        day_sost = sost[0]
        if day_sost.find(',') != -1:
            day_sost = day_sost.split(',')
            draw.text((x, y), day_sost[0] + ',', (255, 255, 255), font=font)
            y += 70
            draw.text((x, y), day_sost[1], (255, 255, 255), font=font)

        else:
            draw.text((x, y), sost[0], (255, 255, 255), font=font)
        y += 70

    if "Давление" in arr:
        draw.text((x, y), davl[0], (255, 255, 255), font=font)
        y += 70

        if y == 340:
            y = 130
            x = 730

    if "Индекс УФ" in arr:
        draw.text((x, y), "УФ: " + yf[0], (255, 255, 255), font=font)
        y += 70

        if y == 340:
            y = 130
            x = 730

    if "Влажность" in arr:
        draw.text((x, y), 'влажность: ' + vlag[0], (255, 255, 255), font=font)
        y += 70

        if y == 340:
            y = 130
            x = 1250

    if "Ветер" in arr:
        draw.text((x, y), wind[0], (255, 255, 255), font=font)

    font = ImageFont.truetype("data/ofont.ru_Letov.ttf", 30)
    for i in range(1, 7):
        x = 100
        y = 620
        draw.text((x + (i-1)*300, 375), days[i], (255, 255, 255), font=font)
        draw.text((x + (i - 1) * 300, y), temp[i], (255, 255, 255), font=font)
        y += 50

        if "Облачность" in arr:
            day_sost = sost[i]

            if day_sost.find(',') != -1:
                day_sost = day_sost.split(',')
                draw.text((x + (i - 1) * 300, y), day_sost[0] + ',', (255, 255, 255), font=font)
                y += 50
                draw.text((x + (i - 1) * 300, y), day_sost[1], (255, 255, 255), font=font)

            else:
                draw.text((x + (i - 1) * 300, y), sost[i], (255, 255, 255), font=font)
            y += 50

        if "Давление" in arr:
            draw.text((x + (i - 1) * 300, y), davl[i], (255, 255, 255), font=font)
            y += 50

        if "Индекс УФ" in arr:
            draw.text((x + (i - 1) * 300, y), "УФ: " +yf[i], (255, 255, 255), font=font)
            y += 50

        if "Влажность" in arr:
            draw.text((x + (i - 1) * 300, y), vlag[i], (255, 255, 255), font=font)
            y += 50

        if "Ветер" in arr:
            draw.text((x + (i - 1) * 300, y), wind[i], (255, 255, 255), font=font)
            y += 50

    img.save("data/hz/res_month.png")

    text = "Картинка😵‍💫"
    return text
# month(['Влажность', 'Облачность', 'Индекс УФ', 'Давление', 'Ветер'])