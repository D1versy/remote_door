import logging
import subprocess
import pathlib
import os
from config import OWNER
import threading
import requests
import time


def hot_patch(*args):
    app_path = pathlib.Path().cwd().parent
    logging.info("Hot patching on path %s...", app_path)

    pip_install = "pip install -r requirements.txt"
    unset = "git config --unset http.https://github.com/"
    pull_unshallow = "git pull"
    pull = "git pull"

    subprocess.call(unset, shell=True, cwd=app_path)
    if subprocess.call(pull_unshallow, shell=True, cwd=app_path) != 0:
        logging.info("pulling now...")
        subprocess.call(pull, shell=True, cwd=app_path)

    logging.info("Code is updated, applying hot patch now...")
    subprocess.call(pip_install, shell=True, cwd=app_path)

def add_user(update, context) -> None:
    message = update.message
    username = message.from_user.username
    if username == OWNER:
        # expecting one argument - the id or username of the new user
        if context.args:
            new_user = context.args[0]
            with open("Users.txt", 'a') as file:
                file.write(f"{new_user}\n")
            context.bot.send_message(chat_id=message.chat.id, text=f"User {new_user} has been added.")
        else:
            context.bot.send_message(chat_id=message.chat.id, text="Please provide the user's id or username. \nCommand example:\n/adduser username\n/adduser 111111111")
    else:
        context.bot.send_message(chat_id=message.chat.id, text="You are not authorized to use this command.")

def button_1_function(update, context):
    threading.Thread(target=call_api).start()

def call_api():
    try:
        response_open = requests.get("http://192.168.1.4/30000/15")
        print("OPENED Status code: ", response_open.status_code)
        time.sleep(1)
        response_close = requests.get("http://192.168.1.4/30000/14")
        print("CLOSED Status code: ", response_close.status_code)
    except Exception as ex:
        print("The Door Api is unavailable")

