import logging
from cli.cli import help
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler

# The Updater class continuously fetches new updates from Telegram and passes them on to the Dispatcher class. Creating an Updater object creates a Dispatcher object and links the Dispatcher object to a queue.
# Different handlers can be registered with the Dispatcher object. The Dispatcher object will sort the updates fetched by Updater and accordingly send them to the callback functions defined.

API_KEY = '5121780857:AAHeKLI0Fws_Ajzy-fphB3sgUbFEVOH5Yo8'

# Create an Updater object
updater = Updater(token=API_KEY, use_context=True)

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
# TODO: Use for sending bop links
def inline_query(update: Update, context: CallbackContext):

    query = update.inline_query.query
    print(query)
    help()

    # No query
    if not query:
        return

    # List of result to show inline
    results = list()
    
    # Do this 3 times
    for i in range(3):
        # Generate a bot response to be added to the Inline query's result
        bot_response_text = InputTextMessageContent(query.upper())
        # Create an Inline result object
        inline_result = InlineQueryResultArticle(
                    id=i,
                    title="Bop {num}".format(num=i+1),
                    input_message_content=bot_response_text
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
