import telebot
from telebot import  types
from telebot import apihelper

import requests
from bs4 import BeautifulSoup


DOLLAR_RUB = 'https://www.google.ru/search?newwindow=1&sxsrf=ALeKk02GUH1tPsuqrs8EXFycaSUNHHS4VA%3A1587125215700&source=hp&ei=35uZXvHOKLKVmwWF4o74Bw&q=%D0%BE%D0%B4%D0%B8%D0%BD+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&oq=%D0%BE%D0%B4%D0%B8%D0%BD+%D0%B4%D0%BE%D0%BB%D0%BB&gs_lcp=CgZwc3ktYWIQAxgAMgcIABBGEIICMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAOgcIIxDqAhAnOgQIIxAnOgUIABCDAUooCBcSJDEwOWc4NWcxMTlnMTMyZzcwZzEyNWc5NGcxNThnMTE1ZzE0MkoXCBgSEzFnMmcxZzFnMWcxZzFnMWcxZzFQqAtY5SFgozJoA3AAeACAAY8BiAHiCJIBAzUuNpgBAKABAaoBB2d3cy13aXqwAQo&sclient=psy-ab'
DOLLAR_EURO = 'https://www.google.ru/search?newwindow=1&sxsrf=ALeKk03YUip9Oi0T35AKguRDzKjfqg-xow%3A1587141394599&source=hp&ei=EtuZXpaRIs2RrgSbwZsI&q=доллар+к+евро&oq=доллар+к+&gs_lcp=CgZwc3ktYWIQAxgCMgUIABCDATICCAAyAggAMgIIADICCAAyBQgAEIMBMgIIADICCAAyAggAMgIIADoHCCMQ6gIQJzoECCMQJzoECAAQCjoGCAAQChAqOgcIABBGEIICSicIFxIjMGcxMzBnMTA0ZzEyN2cxMDZnODhnMTA1ZzEwOWc5NWcxMDFKFwgYEhMwZzNnM2cyZzJnMWcyZzJnMWcxUM0VWLZHYNdYaApwAHgAgAGbAYgB7gySAQQxMC43mAEAoAEBqgEHZ3dzLXdperABCg&sclient=psy-ab'
RUB_DOLLAR = 'https://www.google.ru/search?newwindow=1&sxsrf=ALeKk02XWQBPSErvNR5NSz8HEEZUIiKo5g%3A1587143508845&ei=VOOZXpeSM4qmmwWQxojwDg&q=рубль+к+доллару&oq=рубль+к+доллару&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjICCAAyAggAMgcIABAUEIcCMgIIADICCAAyAggAMgIIADICCAAyAggAOgQIABBHOgcIIxDqAhAnOgkIIxAnEEYQ_wE6BAgjECc6BQgAEIMBOggIABAKEAEQKjoGCAAQChABOgQIABBDOgQIABAKOgkIABBDEEYQggI6BwgAEIMBEEM6DAgAEBQQhwIQRhCCAjoJCAAQChBGEIICSi0IFxIpMGcxMzZnMTM2ZzExMWcxNDhnMTMzZzk0ZzEwMWc4MWc5OGc3NGcxMDhKGwgYEhcwZzJnMmcyZzJnMmcxZzFnMWcxZzdnM1CLW1jdnAFgzKcBaAhwAngAgAGfAYgBnhGSAQQxMy45mAEAoAEBqgEHZ3dzLXdperABCg&sclient=psy-ab&ved=0ahUKEwiXjLWo-u_oAhUK06YKHRAjAu4Q4dUDCAw&uact=5'
RUB_EURO = 'https://www.google.ru/search?newwindow=1&sxsrf=ALeKk004yXCzW9SaXtnfuyXohxWqM1el3A%3A1587143531046&ei=a-OZXoKzAoqAk74Prq6h2A0&q=рубль+к+евро&oq=рубль+к+евро&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjICCAAyBwgAEBQQhwIyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAOgQIABBHOgQIIxAnOgUIABCDAToECAAQCkoSCBcSDjgtOTFnMTA2ZzkwZzEzSg0IGBIJOC0xZzFnM2c0UKPzAViM9wFgm4ICaABwBHgAgAFhiAGlA5IBATWYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwjClICz-u_oAhUKwMQBHS5XCNsQ4dUDCAw&uact=5'
EURO_DOLLAR = 'https://www.google.ru/search?newwindow=1&sxsrf=ALeKk01EJwHnYUjm_GP7m4KmyWaTtaWXYw%3A1587141406428&ei=HtuZXvDGGcqgjgbHzLa4Cw&q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&oq=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADoECAAQRzoHCCMQ6gIQJzoFCAAQgwE6BAgAEEM6BggAEAoQAToECAAQCjoGCAAQChAqOgcIABAKEMsBOgsIABAKECoQRhCCAjoGCAAQFhAeOggIABAWEAoQHjoECCMQJzoHCAAQFBCHAjoJCAAQQxBGEIICOgwIABAUEIcCEEYQggJKKAgXEiQwZzEyMWcxMjRnOTNnODhnODhnMTA2ZzEyNWcxMDlnNzVnODZKGQgYEhUwZzNnM2c0ZzRnM2czZzNnMWcxZzZQuPQrWOvALGChxCxoEXABeACAAZwBiAHNFZIBBDIyLjiYAQCgAQGqAQdnd3Mtd2l6sAEK&sclient=psy-ab&ved=0ahUKEwjwzfO98u_oAhVKkMMKHUemDbcQ4dUDCAw&uact=5'
EURO_RUB = 'https://www.google.ru/search?newwindow=1&sxsrf=ALeKk00s1SwvBUvYXA1X5BuWIGQoWs7YWw%3A1587142136876&ei=-N2ZXvyNNcT16QSm2Y7gBQ&q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+&gs_lcp=CgZwc3ktYWIQAxgBMgQIIxAnMgIIADICCAAyBQgAEIMBMgIIADICCAAyAggAMgIIADIHCAAQFBCHAjICCAA6BAgAEEdKDwgXEgs3LTExMGcxMC0xMkoMCBgSCDctMWcxMC0yUKbNU1imzVNgiNlTaABwAngAgAFdiAFdkgEBMZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab'
db = {"DOLLAR_RUB": DOLLAR_RUB,
      "DOLLAR_EURO": DOLLAR_EURO,
      "RUB_DOLLAR": RUB_DOLLAR,
      "RUB_EURO": RUB_EURO,
      "EURO_RUB": EURO_RUB,
      "EURO_DOLLAR": EURO_DOLLAR}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
current_converted_price = 0


def get_currency_price(value):
    Name = db.get(value)
    full_page = requests.get(Name, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    if Name == RUB_EURO or Name == RUB_DOLLAR:
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 3})
    else:
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})

    return convert[0].text.replace(',', '.')


apihelper.proxy = {'https':'socks5h://96.113.176.101:1080'}

bot = telebot.TeleBot('1226610855:AAEZ25OoNX7U7eT2dYrOUcEflJMUtEICwvE')



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    btn1 = types.KeyboardButton('Доллар к Рублю')
    btn2 = types.KeyboardButton('Доллар к Евро')
    btn3 = types.KeyboardButton('Рубль к Доллару')
    btn4 = types.KeyboardButton('Рубль к Евро')
    btn5 = types.KeyboardButton('Евро к Рублю')
    btn6 = types.KeyboardButton('Евро к Доллару')
    markup.add(btn1, btn2, btn3,btn4, btn5, btn6)
    send_mess = f"<b>Привет {message.from_user.first_name} {message.from_user.last_name}</b>!\nВыбирай кнопку?"
    bot.send_message(message.chat.id,send_mess,parse_mode='html',reply_markup=markup)

@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()
    print(get_message_bot)
    if get_message_bot == "доллар к рублю":
        final_message = "1 доллар = "+get_currency_price("DOLLAR_RUB")+" рублей"
    elif get_message_bot == "доллар к евро":
        final_message = "1 доллар = "+get_currency_price("DOLLAR_EURO")+" евро"
    elif get_message_bot == "рубль к доллару":
        final_message = "1 рубль = "+get_currency_price("RUB_DOLLAR")+" долларов"
    elif get_message_bot == "рубль к евро":
        final_message = "1 рубль = "+get_currency_price("RUB_EURO")+" евро"
    elif get_message_bot == "евро к рублю":
        final_message = "1 евро = "+get_currency_price("EURO_RUB")+" рублей"
    elif get_message_bot == "евро к доллару":
        final_message = "1 евро = "+get_currency_price("EURO_DOLLAR")+" долларов"
    else:
        final_message = "Нажми на кнопку, не пиши сам"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('Доллар к Рублю')
    btn2 = types.KeyboardButton('Доллар к Евро')
    btn3 = types.KeyboardButton('Рубль к Доллару')
    btn4 = types.KeyboardButton('Рубль к Евро')
    btn5 = types.KeyboardButton('Евро к Рублю')
    btn6 = types.KeyboardButton('Евро к Доллару')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, final_message, parse_mode='html',reply_markup=markup)



bot.polling(none_stop=True)
