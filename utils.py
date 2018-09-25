from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings


def get_user_smile(user_data):
    if 'smile' in user_data:
        return user_data['smile']
    else:
        user_data['smile'] = emojize(
            choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['smile']


def get_keyboard():
    contact_button = KeyboardButton('Send contact', request_contact=True)
    location_button = KeyboardButton('Send location', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
        ['Send cat', 'Change avatar'],
        [contact_button, location_button]
    ], resize_keyboard=True
    )
    return my_keyboard
