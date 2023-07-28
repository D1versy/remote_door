from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from config import TOKEN, OWNER
from tasks import add_user, button_1_function


def read_users_from_file(filename):
    with open(filename, 'r') as file:
        users = file.read().splitlines()
    return users

def send_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Open", callback_data='1')
            # InlineKeyboardButton("Option 2", callback_data='2'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='🔘 Tap to Open the door 🔘', reply_markup=reply_markup)

def start(update: Update, context: CallbackContext) -> None:
    send_keyboard(update, context)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    authorized_users = read_users_from_file("Users.txt")

    if query.data == '1':
        if str(query.from_user.id) in authorized_users or query.from_user.username in authorized_users:
            query.answer(text="Access granted.", show_alert=False)
            button_1_function(update, context)
        else:
            query.answer(text="Access denied.", show_alert=False)



def patch_handler(update, context):
    message = update.message
    username = message.from_user.username
    chat_id = message.chat.id
    if username == OWNER:
        context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        context.bot.send_message(chat_id, "Fixed")
    else:
        context.bot.send_message(chat_id=message.chat.id, text="You are not authorized to use this command.")

def info_handler(update, context):
    message = update.message
    username = message.from_user.username
    chat_id = message.chat.id
    user_id = message.from_user.id
    context.bot.send_message(chat_id, text=f'username: {username}\nuser id: {user_id}')

def help_handler(update, context):
    update.message.reply_text('BOT Commands : /start\n/info\n/adduser\n/patch')


def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('patch', patch_handler, run_async=True))
    dispatcher.add_handler(CommandHandler('info', info_handler, run_async=True))
    dispatcher.add_handler(CommandHandler('adduser', add_user, pass_args=True, run_async=True))
    dispatcher.add_handler(CommandHandler('help', help_handler, run_async=True))
    dispatcher.add_handler(MessageHandler(Filters.text, send_keyboard))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    banner = "Welcome to Door bot"
    print(banner)
    main()
