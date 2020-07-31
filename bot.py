import telebot
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime, date
import time

bot = telebot.TeleBot('BOT-TOKEN.')
start = date(2020, 7, 30)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Это бот, который показывает минимальную и максимальную температуру воздуха за сегодняшний день. Теперь тебе не нужно заходить на погодные сайты - просто напиши /pogoda, и бот всё тебе раскажет. Возможно, в будущем он сможет давать больше информации (если это кому-нибудь будет нужно).')

@bot.message_handler(commands=['pogoda'])
def pogoda_message(message):
    bot.send_message(message.chat.id, 'Если я не выйду на связь через 5 минут - звоните в полицию.')
    global start, date
    date = date.today()
    delta = (date - start).days
    n = 11856 + delta


    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36.' }


    request = requests.get('https://www.gismeteo.ua/ua/weather-enerhodar-' + str(n), headers = headers)
    time.sleep(10)
    html = BS(request.content, 'html.parser')


    element = html.select('.tabtemp_0line_inner')
    spisok = []
    for temp in html.select('.value > .unit_temperature_c'):
        spisok.append(temp)
    t1 = spisok[0].text
    t2 = spisok[1].text
    bot.send_message(message.chat.id, "Min: " + t1 + "°C Max: " + t2 + '°C.')

try:
    bot.polling(none_stop=True, interval=0)
except:
    pass
