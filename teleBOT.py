import telebot
import requests

bot = telebot.TeleBot('7555775755:AAG9E9f7CB9Y71xHETNAdRJgAtCT3dXqPL4')

start_txt = 'Привет! Это бот прогноза погоды. \n\nОтправьте боту название города и он скажет, какая там температура и как она ощущается.'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Доступные команды:\n"
        "/start - Начать общение с ботом.\n"
        "/help - Показать это сообщение.\n"
        "Просто отправьте название города, чтобы получить прогноз погоды."
    )
    bot.send_message(message.from_user.id, help_text, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()

    if weather_data['cod'] != 200:
        bot.send_message(message.from_user.id, 'Город не найден. Попробуйте еще раз.')
        return

    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
    w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
    bot.send_message(message.from_user.id, w_now)
    bot.send_message(message.from_user.id, w_feels)

    # Отправка картинки в зависимости от температуры
    if temperature < 0:
        with open('snow.png', 'rb') as photo:
            bot.send_photo(message.from_user.id, photo)
    else:
        with open('sunny.png', 'rb') as photo:
            bot.send_photo(message.from_user.id, photo)

    wind_speed = round(weather_data['wind']['speed'])
    if wind_speed < 5:
        bot.send_message(message.from_user.id, '✅ Погода хорошая, ветра почти нет')
    elif wind_speed < 10:
        bot.send_message(message.from_user.id, '☁️ На улице ветрено, оденьтесь чуть теплее')
    elif wind_speed < 20:
        bot.send_message(message.from_user.id, '❗️ Ветер очень сильный, будьте осторожны, выходя из дома')
    else:
        bot.send_message(message.from_user.id, '⚡️ На улице шторм, на улицу лучше не выходить')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print('Сработало исключение!', e)