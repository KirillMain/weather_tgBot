from bs4 import BeautifulSoup
import lxml
import requests
import re
import os.path
import time
import ast


def w_today(check=False):

    if not check:

        arr_time = []
        arr_temp = []
        arr_sost = []
        arr_wind = []
        arr_vlag = []
        arr_davl = []
        arr_yf = []

        print("eshkereeee")
        url = 'https://pogoda.mail.ru/prognoz/samara/24hours/'
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79"
        }

        req = requests.get(url, headers)
        src = req.text

        with open("data/w_today.html", 'w', encoding="utf-8") as f:
            f.writelines(src)

        with open("data/w_today.html", "r", encoding='utf-8') as f:
            src = f.read()
        soup = BeautifulSoup(src, features="lxml")

        wtime = soup.find_all(class_="p-forecast__item p-forecast__item_time p-forecast__grid-content")
        for i in wtime:
            arr_time.append(i.text)

        wtemp_wsost = soup.find_all(class_="p-forecast__item p-forecast__item_temperature p-forecast__grid-content")
        for i in wtemp_wsost:
            qwe = i.text.split("°")
            arr_temp.append(str(f"{qwe[0]}°"))
            arr_sost.append(qwe[1][0].upper() + qwe[1][1::])

        wwind = soup.find_all(class_="p-forecast__item p-forecast__item_nowrap "
                                     "p-forecast__item_hide-on-touch p-forecast__grid-content")
        for i in wwind:
            qwe = i.text.split("м/с")
            arr_wind.append(qwe[0] + "м/с " + qwe[1])

        wvlag = soup.find_all(class_="p-forecast__item p-forecast__item_hide-on-touch p-forecast__grid-content")
        k = 0
        for i in wvlag:
            k += 1
            if k % 2 == 0:
                continue
            arr_vlag.append(i.text)

        wdavl = soup.find_all(class_="p-forecast__item p-forecast__item_nowrap p-forecast__item_hide-on-desktop-s "
                                     "p-forecast__item_hide-on-touch p-forecast__grid-content")
        for i in wdavl:
            arr_davl.append(i.text)

        wyf = soup.find(class_="icon icon_svg p-forecast__icon p-forecast__icon_uv").find_parent().text
        for i in range(0, 24):
            arr_yf.append(wyf)

        d = {"arr_time": arr_time, "arr_temp": arr_temp, "arr_sost": arr_sost,
             "arr_vlag": arr_vlag, "arr_wind": arr_wind, "arr_davl": arr_davl, "arr_yf": arr_yf}

        with open('data/dict_today.txt', 'w', encoding='utf-8') as f:
            f.write(str(d))

    else:
        with open("data/dict_today.txt", 'r', encoding='utf-8') as f:
            d = ast.literal_eval(f.read())

    return d


def w_info_today(check=False):

    timee = time.ctime(time.time()).split()

    if not check:
        print("eshkereeee2")
        url = "https://pogoda.mail.ru/prognoz/samara/"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79"
        }

        req = requests.get(url, headers, proxies={'http':'','https':''})
        src = req.text
        soup = BeautifulSoup(src, features="lxml")

        head1 = soup.find(class_="information__header__left__date").text
        head = head1.replace('\n', '').replace('\t', '')[:-7]

        head2 = soup.find(class_="information__content__temperature").text
        temp = head2.replace('\n', '').replace('\t', '')

        head3 = soup.find_all(class_="information__content__additional__item")[2].text
        cloudy = head3.replace('\n', '').replace('\t', '')

        head4 = soup.find(class_="information__content__additional__item").text
        feel = head4.replace('\n', '').replace('\t', '')

        head5 = soup.find_all(class_="information__content__additional__item__info "
                                     "information__content__additional__item__info_visible")[1].text
        info = head5.replace('\n', '').replace('\t', '')

        arr = [head, temp, cloudy, feel, info]
        with open("data/list_info_today.txt", 'w', encoding="utf-8") as f:
            f.writelines(str(arr))

    else:
        with open("data/list_info_today.txt", 'r', encoding="utf-8") as f:
            arr = ast.literal_eval(f.read())
    timee = timee[3][:-3]  # закоментить если след строки раскоментишь
    # timee = timee[3][:-3].split(':')
    # t = int(timee[0]) + 4
    # if t > 23:
    #     t -= 24
    # t = str(t)
    # if len(t) == 1:
    #     timee = f'0{t}:{timee[1]}'
    # else:
    #     timee = f'{t}:{timee[1]}'

    arr[0] += ', ' + timee

    return arr


def w_month(check=False):
    if not check:
        arr_days = []
        arr_sost = []
        arr_temp = []
        arr_vlag = []
        arr_wind = []
        arr_davl = []
        arr_yf = []

        print("eshkereeee")
        url = 'https://pogoda.mail.ru/prognoz/samara/14dney/'
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79"
        }

        req = requests.get(url, headers)
        src = req.text

        with open("data/w_month.html", 'w', encoding="utf-8") as f:
            f.writelines(src)

        with open("data/w_month.html", "r", encoding='utf-8') as f:
            src = f.read()
        soup = BeautifulSoup(src, features="lxml")

        days = soup.find_all("span", class_="hdr__inner")
        for i in days:
            qwe = i.text.split()
            if qwe[0] == "Сегодня":
                arr_days.append(qwe[2] + " " + qwe[3][:-1])
            else:
                arr_days.append(qwe[0] + " " + qwe[1][:-1])

        all = soup.find_all(class_="p-flex__column p-flex__column_percent-16")
        vlag = soup.find(style="background-image: url(/img/icon/svg/weather_b.svg)")
        yf = soup.find("use", {"xlink:href": "/-/4c6415b7/bem/web/web.bundles/common/common.svg#icon_forecast_uv"})
        icount = 0
        boolean = False
        for i in all:
            if boolean:
                vlag = vlag.find_next(style="background-image: url(/img/icon/svg/weather_b.svg)")
                yf = yf.find_next("use",
                                  {"xlink:href": "/-/4c6415b7/bem/web/web.bundles/common/common.svg#icon_forecast_uv"})

            if icount == 2:
                qwe = i.text
                temp = re.findall(r'\+\d{1,2}°', qwe)[0]
                arr_temp.append(temp)
                sost = re.findall(r'°.*ощ', qwe)[0].split("ощ")[0][1:]
                arr_sost.append(sost)
                wind = re.findall(r'\d{1,3} м/с \D-\D|\d{1,3} м/с \D', qwe)[0]
                arr_wind.append(wind)
                davl = re.findall(r'\d* мм рт\. ст\.', qwe)[0]
                arr_davl.append(davl)
                arr_yf.append(yf.find_parent().find_parent().find_parent().text)
                arr_vlag.append(vlag.find_parent().text)
                icount = -2
            icount += 1
            boolean = True

        d = {"arr_days": arr_days, "arr_temp": arr_temp, "arr_sost": arr_sost,
             "arr_vlag": arr_vlag, "arr_wind": arr_wind, "arr_yf": arr_yf,
             "arr_davl": arr_davl}

        with open('data/dict_month.txt', 'w', encoding='utf-8') as f:
            f.write(str(d))

    else:
        with open("data/dict_month.txt", 'r', encoding='utf-8') as f:
            d = ast.literal_eval(f.read())

    return d
