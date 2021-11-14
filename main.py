import telebot
from extensions import CurrencyConvert, APIException
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    text = "Чтобы начать конвертировать валюту введите команду боту в следующем формате: \n <имя валюты цену " \
           "который вы хотите узнать> <имя валюты в которой надо узнать цену узнаваемой валюты> <количество " \
           "узнаваемой валюты>\n" \
           "Доступные валюты /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def send_message(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise APIException("Должно быть 3 параметра")
        quote, base, amount = values
        total_base = CurrencyConvert.get_price(base, quote, amount)
        amount = float(amount)
        total_base *= amount
        total_base = float(total_base)
    except APIException as a:
        bot.reply_to(message, f"Ошибка пользователя \n{a}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n{e}.")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()
