import telebot
import telebot.formatting
from music_searcher import download_track, print_all_tracks
import os

bot = telebot.TeleBot(os.getenv("TOKEN"))

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Введите название песни.')

@bot.message_handler()
def print_tracks(message, f=None):

    tracks_list = print_all_tracks(message.text)

    markup = telebot.types.InlineKeyboardMarkup()

    for track_title in tracks_list.values():
        markup.add(telebot.types.InlineKeyboardButton(text=track_title, callback_data=track_title))


    bot.send_message(message.chat.id, text='Выберите подходящий трек:', reply_markup=markup)

    if f == 'inline':
        return tracks_list

        
    

@bot.callback_query_handler(func=lambda call: True)
def send_track(call):
    tracks_list = print_tracks('', 'inline')
    for key, value in tracks_list.items():
        if call.data == value:
            track = key;

    filename = download_track(track)

    track_file = open(filename, 'rb')
    bot.answer_callback_query(call.id, "Download.")

    bot.send_audio(call.chat.id, track_file)

bot.infinity_polling()