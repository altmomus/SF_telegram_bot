import telebot

from config import TOKEN
from extensions import RequestsToApi

bot = telebot.TeleBot(TOKEN)

class APIException(Exception):
    def __init__(self, text):
        self.txt = text


@bot.message_handler(commands=["start", "help"])
def start_or_help_bot(message):
    bot.send_message(message.chat.id, "Здравствуйте, при вводе команды /values, выведется информация обо всех валютах.\n"
                                      "Отправьте сообщение в виде <имя валюты цену которой вы хотите узнать> "
                                      "<имя валюты в которой вам надо узнать цену первой валюты> <количество первой валюты>. "
                                      "Пример: USD RUB 1 или EUR RUB 1.")


@bot.message_handler(commands=["values"])
def get_information_about_values(message):
    ex = RequestsToApi()
    values_data = ex.get_amount_values()
    bot.send_message(message.chat.id, f"1 USD = {int(values_data[0])} RUB\n"
                                      f"1 EUR = {int(values_data[1])} RUB")


@bot.message_handler(content_types="text")
def convert_values(message):
    user_data_for_converting = message.text.split(" ")

    try:
        if user_data_for_converting[0] not in ["RUB", "EUR", "USD"]:
            raise APIException("Вы неверно ввели первую валюту")
        elif user_data_for_converting[1] not in ["RUB", "EUR", "USD"]:
            raise APIException("Вы неверно ввели вторую валюту")

        int(user_data_for_converting[2])  # выдаст ValueError если не число

        ex = RequestsToApi()
        values_data = ex.get_price(user_data_for_converting[0], user_data_for_converting[1], user_data_for_converting[2])
        bot.send_message(message.chat.id, f"{user_data_for_converting[2]} {user_data_for_converting[0]} = "
                                          f"{values_data} {user_data_for_converting[1]}")
    except APIException as txt:
        bot.send_message(message.chat.id, f"{txt}")
    except ValueError:
        bot.send_message(message.chat.id, "Вы не ввели количество валюты")


bot.polling()
