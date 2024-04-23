import telebot
from telebot import types
from currency_converter import CurrencyConverter


bot = telebot.TeleBot('6687879886:AAEBOlMoolOojmMstUC2NMYtTsC9VoiGODk')
currency = CurrencyConverter()


amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, enter the amount')
    bot.register_next_step_handler(message, sum)


def sum(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid value, enter only a number')
        bot.register_next_step_handler(message, sum)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('others', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Select a value', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Invalid value, enter only a number')
        bot.register_next_step_handler(message, sum)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'It is {round(res, 2)}')
        bot.register_next_step_handler(call.message, sum)
    else:
        bot.send_message(call.message.chat.id, 'Enter currencies with a slash. ex: ABC/ABC')
        bot.register_next_step_handler(call.message, mycurrency)


def mycurrency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'It is {round(res, 2)}')
        bot.register_next_step_handler(message, sum)
    except Exception:
        bot.send_message(message.chat.id, 'Something is wrong, try again')
        bot.register_next_step_handler(message, sum)


bot.polling(none_stop=True)