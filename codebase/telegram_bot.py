from config import *
global bot, conn, cur
import time

telegram_bot_token = "5413711929:AAFwVMM9jkYwsnHvkiUNwAUQSrvuSsBqZAc"
updater = Updater(token=telegram_bot_token, use_context=True)
bot = Bot(token=telegram_bot_token)
dispatcher = updater.dispatcher
conn = None
cur = None

def start_db_connection():
    global conn, cur
    start_commands = ["""CREATE TABLE IF NOT EXISTS user_chats(
   user_name TEXT PRIMARY KEY,
   chat_id TEXT,
   last_time_sent TEXT,
   UNIQUE(user_name, chat_id));
"""]
    try:
        conn = sqlite3.connect("user_chat_db", check_same_thread=False)
        cur = conn.cursor()
        print(f"SQLite3 created connection, sqlite3 version:", sqlite3.version)
    except Error as e:
        print(f"Failed to crete connection with db:", e)
    for command in start_commands:
        cur.execute(command)
        conn.commit()


def clear_db():
    global conn, cur
    cur.execute("""DELETE FROM user_chats;""")
    conn.commit()


def close_db():
    conn.close()

def add_user(update):
    global conn, cur
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    print(f"Adding user user_id: {user_id}, user_name: {user_name}, chat_id: {chat_id}")
    cur.execute(f'INSERT OR IGNORE INTO user_chats VALUES("{user_name}", "{chat_id}", "...");')
    conn.commit()
    return chat_id

def start(update, context):
    chat_id = add_user(update)
    context.bot.send_message(chat_id=chat_id, text="Hello there. I am a perfect HSE bot and i will provide you with everything you need. Print /help command to see everything i can do!")

def create_chat(chat_name):
    print("creating chat")
    chat = Chat(type="GROUP", title=chat_name)
    chat.bot.get
    

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"""I have a random set of tasks:
    /start - start command
    /help  - print help, lol
    /chats - print useful HSE chats list
    /share - print some text as an argument to this and share your idea with random user!
    /count - start a timer which is definetely not annoying, maybe something cool happends in the end
    /joke  - i have no humor so it was copypasted from Google""")

STOP_WORDS = ["fuck", "bitch", "dick", "херня", "хуй", "сука"]
SECRET_WORDS = ["Christmas", "Новы", "Год", "Поздрав"]
def any_stop_words(words, inp):
    for word in words:
        if word in inp:
            return True
    return False

def send_text(update, context):
    print(update.message)
    global STOP_WORDS
    if any_stop_words(SECRET_WORDS,  update.message.text):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Yeeeey!)")
    elif any_stop_words(STOP_WORDS, update.message.text):
        context.bot.send_message(chat_id=update.effective_chat.id, text="┐(￣ヮ￣)┌")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Unfortunately i am too stupid to understand any of it")
        
def send_chat_list(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="HSE chats are useless so it's empty")
     
        
def send_nudes(update, context):
    global conn, cur
    print(update.message.from_user)
    user_name = update.message.from_user.first_name
    idea = update.message.text[6:]
    print(idea)
    print("sending great idea")
    cur.execute('''SELECT chat_id FROM user_chats ORDER BY RANDOM() LIMIT 1;''')
    chat_id = cur.fetchall()[0][0]
    context.bot.send_message(chat_id=chat_id, text=f"Hello there! You've been chosen as a random sacrifice for {user_name}'s idea!\nHere it is: {idea}")    

from concurrent.futures import ProcessPoolExecutor
p = ProcessPoolExecutor(3)
  
async def count_to_ten(update, context):
    chat_id = update.effective_chat.id
    for i in range(1, 11):
        context.bot.send_message(chat_id=chat_id, text = f"{i}...")
        time.sleep(1)
    context.bot.send_message(chat_id=chat_id, text = " !!! Merry Christmas !!! ")

def smth(update, context):
    """
    global p
    asyncio.get_event_loop().run_in_executor(p, count_to_ten, *args)
    """
    context.bot.send_message(chat_id= update.effective_chat.id, text = "Look, technically i am not using asyncio BUT the module i'm using has obvious event handlers and can do shit simultaniosly. Therefore, it's actually asynchronous. Don't question it.")

def joke(update, context):
    context.bot.send_message(chat_id= update.effective_chat.id, text = "Don’t challenge Death to a pillow fight. Unless you’re prepared for the reaper cushions. *chokes from cringe*")    

@asyncio.coroutine
def main():
    start_db_connection()
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("chats", send_chat_list))
    dispatcher.add_handler(CommandHandler("share", send_nudes))
    dispatcher.add_handler(CommandHandler("count", smth))
    dispatcher.add_handler(CommandHandler("joke", joke))
    dispatcher.add_handler(MessageHandler(Filters.text, send_text))
    updater.start_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
