import telebot
from config import keys, TOKEN
from extensions import ConversionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f'Чтобы начать работу веди команду боту в следующем формате:\n <имя валюты> \
<в какую перевести> <количество переводимой валюты>\n Увидеть список всех доступных\
валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        params = message.text.split(' ')

        if len(params) != 3:
            raise ConversionException('Неверное количество параметров')

        quote, base, amount = params
        total_base = CurrencyConverter.get_price(quote, base, amount)

    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
        

bot.polling()
