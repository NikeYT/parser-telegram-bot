import telebot
import requests
import time
import config

bot = telebot.TeleBot(config.TOKEN)
found_words = {} # словарь для хранения информации о найденных словах / dictionary for storing information about found words

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(chat_id=message.chat.id, text="Привет! Я бот для парсинга слов в канале и отправки их в личные сообщения. Напиши мне любое сообщение, чтобы начать поиск.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    words = ["w1", "w2", "w3"]
    text = message.text.lower()
    for word in words:
        if word in text and (chat_id, word) not in found_words:
            bot.send_message(chat_id=chat_id, text=f"Найдено слово '{word}' в сообщении '{text}'")
            found_words[(chat_id, word)] = True

def get_updates():
    # Запрос обновлений из канала с идентификатором CHANNEL_ID / Request updates from a channel with the CHANNEL_ID
    url = f"https://api.telegram.org/bot{config.TOKEN}/getUpdates?offset=-1&chat_id=-{config.ID}"
    response = requests.get(url)
    data = response.json()

    # Обработка полученных сообщений / Handling received messages
    for message in data["result"]:
        chat_id = message["message"]["chat"]["id"]
        text = message["message"]["text"].lower()
        words = ["w1", "w2", "w3"]
        for word in words:
            if word in text not in found_words:
                bot.send_message(chat_id=chat_id, text=f"Найдено слово '{word}' в сообщении '{text}'")
                found_words[(chat_id, word)] = True

while True:
    try:
        get_updates() # Получение обновлений из канала / Getting updates from a channel
        time.sleep(5) # Задержка между запросами / Delay between requests

    except Exception as e:
        print(e)
        time.sleep(5)

bot.polling()
