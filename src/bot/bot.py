import logging
import os
import configparser
import validators
from cli.cli import all_links_conversion
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from urllib.parse import urlparse

# The Updater class continuously fetches new updates from Telegram and passes them on to the Dispatcher class. Creating an Updater object creates a Dispatcher object and links the Dispatcher object to a queue.
# Different handlers can be registered with the Dispatcher object. The Dispatcher object will sort the updates fetched by Updater and accordingly send them to the callback functions defined.

config = configparser.ConfigParser()
config.read('.env')
boplinkbot_token = config['TELEGRAM_BOPLINKBOT_TOKEN']['TOKEN']

# Create an Updater object
updater = Updater(token=boplinkbot_token, use_context=True)

# Fetch Dispatcher object
dispatcher = updater.dispatcher

# Create a logger object to know when and why things are not working as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Function for handling /start command
def start(update: Update, context: CallbackContext):
    bot_response_text = "Hello there! My name is Bop Link"
    context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response_text)

# Function for responding to unknown commands/messages
def unknown(update: Update, context: CallbackContext):
    bot_response_text = "Sorry, I only respond to inline links in chats."
    context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response_text)

# Function for responding to inline queries
def inline_query(update: Update, context: CallbackContext):


    query = update.inline_query.query
    print(query)

    # No valid input 
    if not validators.url(query):
        print("Not a valid URL: {}".format(query))
        return
    
    # Get all the links given the user URL
    all_links_dict = all_links_conversion(query)
    # If dictionary is empty, that means an error was hit. No results should be sent back to the end user.
    if not all_links_dict:
        return

    # List of result to show inline
    results = list()
    
    # Iterate through the dictionary
    for index, key in enumerate(all_links_dict):
        # If no link was found for this particular streaming service
        if all_links_dict[key] == None:
            pass
        else:
            # Generate a bot response as the URL to be added to the Inline query's result
            inline_response_text = InputTextMessageContent(all_links_dict[key])
            # Create an Inline result object
            inline_result = InlineQueryResultArticle(
                        id=index,
                        title=key.title(),
                        input_message_content=inline_response_text
                    )

            # Append this result to the results list
            results.append(inline_result)

    # Respond inline query with the results list
    context.bot.answer_inline_query(update.inline_query.id, results)

# Create a command handler which connects the Start command with the start method
start_handler = CommandHandler('start', start)
# Create a command handler which connects messages and unknown commands to some response
unknown_handler = MessageHandler(Filters.command & Filters.text, unknown)
# Create the inline response handler
inline_handler = InlineQueryHandler(inline_query)
# Tell the dispatcher object about the handlers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(inline_handler)
# Must be added last because priority of handling matters
dispatcher.add_handler(unknown_handler)

# Let the updater run
updater.start_polling()
