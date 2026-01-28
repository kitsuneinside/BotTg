from bot_info import *
from datetime import datetime, timedelta
from sticker import *

USER = {}

THROTTLING = {}

CDKEYBORDS = {}

START_TIME = {}

EVENT_PHHOTO = ""
EVENT_NAME = ""

DELTA = timedelta(seconds=THROTTLE_DELEY)
COLLDOWN = timedelta(minutes=COOLDOWN_DELEY)
SHUTDOWNUSER = timedelta(minutes=SHUTDOWN_DELEY)


def throttle(f):
    def inner(message):
        if message.chat.id in THROTTLING:
            current_time = datetime.now()
            if current_time - THROTTLING[message.chat.id] > DELTA:
                THROTTLING[message.chat.id] = datetime.now()
                return f(message)

    return inner


def colldown_decorator(f):
    def inner(message):

        if message.chat.id in CDKEYBORDS:
            current_time = datetime.now()
            if current_time - CDKEYBORDS[message.chat.id] > COLLDOWN:
                CDKEYBORDS[message.chat.id] = datetime.now()
                return f(message)
            else:
                bot.send_message(message.chat.id, "А щоб тебе підняло і гепнуло.")
                bot.send_message(message.chat.id, "Вже підганяю цього лентюха!!!")
                bot.send_sticker(message.chat.id, sticker=stickers[1])
                return bot.delete_message(message.chat.id, message.message_id)

    return inner


def start_time(f):
    def inner(message):
        if message.chat.id in START_TIME:
            current_time = datetime.now()
            if current_time - START_TIME[message.chat.id] < SHUTDOWNUSER:
                return f(message)
            else:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(
                    message.chat.id, "На жаль, час дії сплинув. Відскануй QR ще раз."
                )
                bot.send_sticker(message.chat.id, sticker=stickers[2])

    return inner
