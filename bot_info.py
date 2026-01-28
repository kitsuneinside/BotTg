import telebot
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_API = os.getenv("BOT_TOKEN")

CHANNEL = os.getenv("CHANNEL_TOKEN")


THROTTLE_DELEY = 1  # seconds
COOLDOWN_DELEY = 1  # minutes
SHUTDOWN_DELEY = 10  # minutes


NAME_FILE = "table.json"

bot = telebot.TeleBot(TOKEN_API)

CHANNEL_ID = CHANNEL

filename = NAME_FILE

web = {
    "kitchen": "https://whitefox.postershop.me",
    "bar": "https://menu.ps.me/BpJgi6y2iUY/category/41",
    "hookah": "https://menu.ps.me/BpJgi6y2iUY/category/69",
    "feedback_google": "https://www.google.com/maps/place/White+Fox/@48.9202015,24.7028699,17z/data=!4m8!3m7!1s0x4730"
                       "c1176eb9e2ed:0x923d8272d263b889!8m2!3d48.9201981!4d24.7077408!9m1!1b1!16s%2Fg%2F11fj531tll?"
                       "entry=ttu",
}
