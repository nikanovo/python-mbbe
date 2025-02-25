import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as b

bot = telebot.TeleBot('8078422610:AAHI-iMDiiXgBQKsWpt5jHmSFvj2yR_H_oE')

def get_inf(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')

    news_items = soup.find_all('div', class_='se-material__title se-material__title--size-middle')
    timings = soup.find_all('div', class_='se-news-list-page__item-left')
    news_heads = [c.text for c in news_items][:3]
    links = [c.find_all('a') for c in news_items][:3]
    timing_list = [c.text for c in timings][:3]

    ans = []
    for j in range(3):
        if len(timing_list[j].split()) == 1:
            date = timing_list[j].strip() + ' (сегодня)'
        else:
            ind = timing_list[j].find(':') + 3
            date = timing_list[j][:ind] + f' ({timing_list[j][ind:ind + 6].strip()})'
        head = news_heads[j].strip()
        text = str(links[j][0]).split('"')[1]
        ans.append([date, head, text])
    return ans[::-1]

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет! Я бот спортивных новостей. \nИспользуйте команду */sport* для просмотра последних *спортивных* событий.', parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'q_1':
            URL = 'https://m.sport-express.ru/futsal/news/?isEditorialChoice=1'
            inf = get_inf(URL)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'{inf[0][0]} \n{inf[0][1]} \n[Читать далее]({inf[0][2]})', parse_mode="Markdown")
            inf = inf[1:]
            for l in inf:
                bot.send_message(call.message.chat.id, f'{l[0]} \n{l[1]} \n[Читать далее]({l[2]})', parse_mode="Markdown")
        elif call.data == 'q_2':
            URL = 'https://www.sport-express.ru/hockey/news/?isEditorialChoice=1'
            inf = get_inf(URL)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'{inf[0][0]} \n{inf[0][1]} \n[Читать далее]({inf[0][2]})', parse_mode="Markdown")
            inf = inf[1:]
            for l in inf:
                bot.send_message(call.message.chat.id, f'{l[0]} \n{l[1]} \n[Читать далее]({l[2]})', parse_mode="Markdown")
        elif call.data == 'q_3':
            URL = 'https://www.sport-express.ru/basketball/news/?isEditorialChoice=1'
            inf = get_inf(URL)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'{inf[0][0]} \n{inf[0][1]} \n[Читать далее]({inf[0][2]})', parse_mode="Markdown")
            inf = inf[1:]
            for l in inf:
                bot.send_message(call.message.chat.id, f'{l[0]} \n{l[1]} \n[Читать далее]({l[2]})', parse_mode="Markdown")

@bot.message_handler(commands=['sport'])
def sport_command(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('Последние новости Футзала', callback_data='q_1')
    item2 = types.InlineKeyboardButton('Последние новости Хоккея', callback_data='q_2')
    item3 = types.InlineKeyboardButton('Последние новости Баскетбола', callback_data='q_3')
    markup.add(item, item2, item3)

    bot.send_message(message.chat.id, 'Вы можете выбрать:', reply_markup=markup)

bot.infinity_polling()
