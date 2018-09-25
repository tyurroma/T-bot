import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import settings
from handlers import *


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Bot is starting')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('planet', planet, pass_args=True))
    dp.add_handler(CommandHandler(
        'cat', send_cat_picture, pass_user_data=True))
    dp.add_handler(CommandHandler('calc', calculate, pass_args=True))
    dp.add_handler(CommandHandler('wordcount', wordcount, pass_args=True))
    dp.add_handler(RegexHandler(
        '^(Send cat)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Change avatar)$',
                                change_avatar, pass_user_data=True))
    dp.add_handler(RegexHandler('^(.*=$)$', calculate))
    dp.add_handler(MessageHandler(Filters.contact,
                                  get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location,
                                  get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(
        Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
