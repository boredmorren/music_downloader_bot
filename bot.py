import telebot
import telebot.formatting
from music_searcher import download_track, print_all_tracks
import os, zlib, base64

bot = telebot.TeleBot(os.getenv("TOKEN"))

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Введите название песни.')

@bot.message_handler()
def print_tracks(message, f=None):

    global tracks_list 
    tracks_list = print_all_tracks(message.text)

    markup = telebot.types.InlineKeyboardMarkup()

    for track_title in tracks_list.values():
        if len(track_title.encode('utf-8')) < 64:
            markup.add(telebot.types.InlineKeyboardButton(text=track_title, callback_data=track_title))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=track_title.split(' - ')[0], callback_data=track_title.split(' - ')[0]))


    bot.send_message(message.chat.id, text='Выберите подходящий трек или исполнителя', reply_markup=markup)      
    

@bot.callback_query_handler(func=lambda call: True)
def send_track(call):
    for key, value in tracks_list.items():
        if call.data == value:
            track = key;


    filename = download_track(track)

    track_file = open(filename, 'rb')
    bot.answer_callback_query(call.id, "Downloading.")

    bot.send_audio(call.message.chat.id, track_file)
    track_file.close()

    os.remove(filename)

    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

bot.infinity_polling()