import datetime as d
import ephem
from glob import glob
import logging
from random import choice
import re

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def greet_user(bot, update, user_data):
    smile = get_user_smile(user_data)
    user_data['smile'] = smile
    text = 'Hello, {}! With the help of this bot, you can find out ' \
            'in which constellation the planet is today. ' \
            'Just type the command: /planet <planet name>. ' \
            'Something like this: /planet Mars. ' \
            'The list of planets are: Mars, Neptune, Pluto, Saturn, Uranus, Venus, Jupiter. '\
            'Bot can also show what you wrote. ' \
            'Type /cat to see some cats {}' \
            .format(update.message.chat.first_name, smile)

    logging.info(text)
    update.message.reply_text(text, reply_markup=get_keyboard())

def planet(bot, update, args):
    date_today = d.datetime.today()
    planet_name = ' '.join(args)
    planet_name = planet_name.lower()
    try: 
        if planet_name == 'mars':
            planet_name = ephem.Mars(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'neptune':
            planet_name = ephem.Neptune(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])    
        elif planet_name == 'pluto':
            planet_name = ephem.Pluto(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'saturn':
            planet_name = ephem.Saturn(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'uranus':
            planet_name = ephem.Uranus(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'venus':
            planet_name = ephem.Venus(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'jupiter':
            planet_name = ephem.Jupiter(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])    
        else:
            update.message.reply_text('No data')
    except IndexError:
        update.message.reply_text('Enter planet name please! For example, /planet Mars',
                                    reply_markup=get_keyboard()
                                )
        logging.info ('User did not enter a planet')

def talk_to_me(bot, update, user_data):
    smile = get_user_smile(user_data)
    user_text = 'Hello {}! You wrote: {}. {}'.format(update.message.chat.first_name, update.message.text,
                user_data['smile'])
    logging.info('User: {}, Chat id: {}, Message: {}'.format(update.message.chat.username,
                update.message.chat.id, update.message.text))
    update.message.reply_text(user_text, reply_markup=get_keyboard())

def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/*cat*.jpg')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())

def get_user_smile(user_data):
    if 'smile' in user_data:
        return user_data['smile']
    else:
        user_data['smile'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['smile']

def change_avatar(bot, update, user_data):
    if 'smile' in user_data:
        del user_data['smile']
    smile = get_user_smile(user_data)
    update.message.reply_text('Done! {}'.format(smile), reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Done! {}'.format(get_user_smile(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Done! {}'.format(get_user_smile(user_data)), reply_markup=get_keyboard())

def get_keyboard():
    contact_button = KeyboardButton('Send contact', request_contact=True)
    location_button = KeyboardButton('Send location', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Send cat', 'Change avatar'],
                                        [contact_button, location_button]
                                        ], resize_keyboard=True
                                    )
    return my_keyboard

def wordcount(bot, update, args):
    words = ' '.join(args)
    words = re.sub('[«»"!@#$:;.,?]', '', words)
    words = words.split()

    while len(words) != 0:
        update.message.reply_text('Words in your phrase: {}'.format(len(words)), reply_markup=get_keyboard())
        logging.info()
        break
    else:
        update.message.reply_text('Enter some words, please!', reply_markup=get_keyboard())

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Bot is starting')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('planet', planet, pass_args=True))
    dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler('wordcount', wordcount, pass_args=True))
    dp.add_handler(RegexHandler('^(Send cat)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Change avatar)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()