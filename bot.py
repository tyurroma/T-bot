import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
import datetime as d

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def greet_user(bot, update):
    text = 'Hello, {}! With the help of this bot, you can find out ' \
            'in which constellation the planet is today. ' \
            'Just type the command: /planet <planet name>. ' \
            'Something like this: /planet Mars. ' \
            'The list of planets are: Mars, Neptune, Pluto, Saturn, Uranus, Venus, Jupiter. '\
            'Bot can also show what you wrote.' \
            .format(update.message.chat.first_name)
    logging.info(text)
    update.message.reply_text(text)
    update.message.reply_text(instruction)

def planet(bot, update, args):
    date_today = d.datetime.today()
    planet_name = ' '.join(args)
    logging.info(planet_name)
    try: 
        if planet_name == 'Mars':
            planet_name = ephem.Mars(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'Neptune':
            planet_name = ephem.Neptune(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])    
        elif planet_name == 'Pluto':
            planet_name = ephem.Pluto(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'Saturn':
            planet_name = ephem.Saturn(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'Uranus':
            planet_name = ephem.Uranus(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'Venus':
            planet_name = ephem.Venus(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])
        elif planet_name == 'Jupiter':
            planet_name = ephem.Jupiter(date_today)
            update.message.reply_text(ephem.constellation(planet_name)[1])    
        else:
            update.message.reply_text('No data')
    except IndexError:
        update.message.reply_text('Enter planet name please! For example, /planet Mars')
        logging.info ('User did not enter a planet')

def talk_to_me(bot, update):
    user_text = 'Hello {}! You wrote: {}.'.format(update.message.chat.first_name, update.message.text)
    logging.info('User: {}, Chat id: {}, Message: {}'.format(update.message.chat.username,
                update.message.chat.id, update.message.text))
    update.message.reply_text(user_text)

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Bot is starting')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()