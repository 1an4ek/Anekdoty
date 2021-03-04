#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, random, urllib.request, os.path, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

url = 'https://1an4ek.github.io/Anekdoty/'

kb = [[InlineKeyboardButton('Про школу', callback_data = 'school')],
            [InlineKeyboardButton('Про семью', callback_data = 'family')],
            [InlineKeyboardButton('Про политику', callback_data = 'politics')],
            [InlineKeyboardButton('Картинка с котиками', callback_data = 'catz')]]
reply = InlineKeyboardMarkup(kb)
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def openurlfile(filename):
    with urllib.request.urlopen(url + '/' + filename) as uf: 
        x = uf.read().decode('utf-8') 
        x = x.split('\n')
    return x

def start(update, context):   
    update.message.reply_text('Я вас категорически приветствую. \n Выберите тему анекдота', reply_markup = reply)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('А не надо тут такого')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def school(update, context):
    x = openurlfile('school.txt')
    #file = open('school.txt', 'r', encoding = 'utf-8')
    #x = file.readlines()
    #file.close()
    y = random.randrange(0, 6)
    context = '\n'.join(x[y * 7 : y * 7 + 7])
    update.callback_query.message.reply_text(context)
    update.callback_query.message.reply_text('Выберите тему анекдота', reply_markup = reply)

def family(update, context):
    pass
    '''x = openurlfile('family.txt')
    y = random.randrange(0, 2)
    context = '\n'.join(x[y * 7 : y * 7 + 7])
    update.callback_query.message.reply_text(context)
    update.callback_query.message.reply_text('Выберите тему анекдота', reply_markup = reply)'''

def politics(update, context):
    x = openurlfile('politics.txt')
    y = random.randrange(0, 2)
    context = '\n'.join(x[y * 7 : y * 7 + 7])
    update.callback_query.message.reply_text(context)
    update.callback_query.message.reply_text('Выберите тему анекдота', reply_markup = reply)

def catz(update, context):
    num = random.choise(len([name for name in os.listdir(url + 'catz/') if os.path.isfile(name)]))
    coti_url = url + '/catz/' + num 
    update.callback_query.message.bot.send_photo(chat_id = update.callback_query.message.chat.id, photo = coti_url)
    #update.callback_query.message.reply_text('Лови', photo = coti_url)
    update.callback_query.message.reply_text('Выберите тему анекдота', reply_markup = reply)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1641289734:AAG8ey-c98ORi-9BUpIIQZp31eb70mlfsGg", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(school, pattern = 'school'))
    dp.add_handler(CallbackQueryHandler(family, pattern = 'family'))
    dp.add_handler(CallbackQueryHandler(politics, pattern = 'politics'))
    dp.add_handler(CallbackQueryHandler(catz, pattern = 'catz'))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()





if __name__ == '__main__':
    main()
