from sys import platform
from threading import Thread
from tkextrafont import Font
from tkinter import ttk, Tk, Label
from javascript import require, On
from configparser import ConfigParser

config = ConfigParser()
mineflayer = require("mineflayer")

config.read("config.ini")

username = config.get("bot", "name")

def started(stop):
    global bot
    bot = mineflayer.createBot({"host": config.get("server", "host"), "port": config.get("server", "port"), "respawn": True if config.get("bot", "auto_respawn") is 1 else False, "username": username})

    print(f"\033[32m[INFO]: {username} is connecting to {config.get('server', 'host')}...\033[0m")
    
    @On(bot, "login")
    def login(this):
        print(f"\033[32m[INFO]: {username} successfully connected!\033[0m")
        bot.chat("/gamemode creative")
        bot.chat(f"{username} connected!")
        bot.setControlState("jump", True)
        bot.chat(f"{username} started!")
        bot_status.configure(text="The bot is online", font=("ebrima", 20))
        
    @On(bot, "error")
    def error(err, *a):
        print("\033[31m[ERROR]: The bot was unable to connect because of: ", err, a, "\033[0m")

        stop_button.destroy()
        
        global start_button
        start_button = ttk.Button(root, text="Start", command=lambda: start())

        start_button.place(x=5, y=100, width=205)
    
    @On(bot, "kicked")
    def kicked(this, reason, *a):
        print("\033[31m[ERROR]: The bot got kicked because of: ", reason, a, "\033[0m")
        bot.end()

        stop_button.destroy()
        
        global start_button
        start_button = ttk.Button(root, text="Start", command=lambda: start())

        start_button.place(x=5, y=100, width=205)
    
    @On(bot, "chat")
    def handle(this, username, message, *args):
        if username == bot.username:
            return

        elif message.startswith(".help"):
            bot.chat("----- Commands -----\n.stop - Stops the bot\n.start - Starts the bot\n \nINFO: You need to be\n       Admin to use\n       commands!\n-------------------")

        elif message.startswith(".stop"):
            bot.chat(f"{username} stopped!")
            bot.clearControlStates()

        elif message.startswith(".start"):
            bot.chat(f"{username} started!")
            bot.setControlState("jump", True)

def start():
    global bot_, stop_threads

    stop_threads = False
    bot_ = Thread(target=started, args=(lambda: stop_threads,))

    start_button.destroy()
    bot_.start()

    global stop_button
    stop_button = ttk.Button(root, text="Stop", command=lambda: stop())

    stop_button.place(x=5, y=100, width=205)

def stop():
    try:
        bot.quit()
        viewer.quit()
        bot_status.configure(text="The bot is offline", font=("ebrima", 20))
        print("\033[32m[INFO]: The bot successfully stopped!\033[0m")
        stop_button.destroy()

        global start_button
        start_button = ttk.Button(root, text="Start", command=lambda: start())

        start_button.place(x=5, y=100, width=205)

    except:
        pass

root = Tk()
font = Font(file="ebrima.ttf", family="ebrima")
bot_status = Label(root, text="The bot is offline", font=("ebrima", 20))

root.tk.call("source", "forest-dark.tcl")
root.geometry("215x150")
root.resizable(width=False, height=False)
root.title("")
ttk.Style().theme_use("forest-dark")
bot_status.place(x=5, y=30)

global start_button
start_button = ttk.Button(root, text="Start", command=lambda: start())

start_button.place(x=5, y=100, width=205)

if platform == "win32":
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)

root.mainloop()
