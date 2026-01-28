import json
import admin_function_action
import admin_function_message
from DB import (
    db,
    User,
    Actions,
    path,
    db_path,
    init_db,
    folder_name)
import time
from admin_function_message import (
    action_barr,
    planed_message_barr,
    select_all_from_db,
    send_name_event,
    tmp,
    take_name,
    chose_edit,
    name_edit_t,
    name_edit_p,
)
from admin_function_action import (
    chose_action_for_edit,
    name_edit_t_action,
    name_edit_p_in_action,
    select_all_action_from_db,
    add_action_,
    take_name_action_,
)
from decorators import *
from Markup import markupp, edit_menu_markup, types, reyting_markup


callbacks = {
    "action_bar": action_barr,
    "planed_message_bar": planed_message_barr,
    "event_list": select_all_from_db,
    "send_messages_from_users": send_name_event,
    "add_events": tmp,
    "delete_event": take_name,
    "edit_event": chose_edit,
    "edit_text": name_edit_t,
    "edit_photos": name_edit_p,
    "edit_action": chose_action_for_edit,
    "edit_photos_action": name_edit_p_in_action,
    "edit_text_action": name_edit_t_action,
    "action_list": select_all_action_from_db,
    "add_action": add_action_,
    "delete_action": take_name_action_,
}

if not os.path.exists(db_path):
    init_db()
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Створено папку {folder_name}")
    print("Файл БД НЕ існує")

os.makedirs(path, exist_ok=True)

@bot.message_handler(commands=["start"])
def main(message):
    THROTTLING[message.chat.id] = datetime.now()
    CDKEYBORDS[message.chat.id] = datetime.now() - COLLDOWN
    START_TIME[message.chat.id] = datetime.now()

    admins = bot.get_chat_administrators(CHANNEL)
    for admin in admins:
        if admin.user.username == message.from_user.username:
            print("admin detected")
            bot.send_message(
                message.chat.id,
                "Обери що бажаєш редагувати",
                reply_markup=edit_menu_markup,
            )
            print(f"{admin.user.username}")
            return

    with open(filename, "r") as file:
        data = json.loads(file.read())

    try:
        USER[message.chat.id] = data[message.text.split()[-1]]

    except KeyError:
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ',
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2], reply_markup=markupp)

    else:
        bot.send_message(
            message.chat.id, "Привіт я твій особистий помічник ", reply_markup=markupp
        )
        bot.send_message(message.chat.id, f'{emoji["fox_face"]}')
        bot.delete_message(message.chat.id, message.message_id)

    with db:
        users = User.select().where(User.chat_id == message.chat.id).first()
        if users is None:
            User.create(
                id=None,
                chat_id=message.chat.id,
                name=f"{message.from_user.username}",
                flag=True,
            )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data in callbacks:
        callbacks[call.data](call.message)

    elif call.data in ["1", "2", "3", "4", "5"]:
        bot.send_message(CHANNEL_ID, f"Оцінили обслуговування на {call.data} ")


@bot.message_handler(func=lambda message: message.text == f'Меню {emoji["fork_knife"]}')
@throttle
@start_time
def menu(message):

    markup = types.InlineKeyboardMarkup()

    btnkitchen = types.InlineKeyboardButton(
        f'Щось пожерти {emoji["drooling_face"]}', url=web["kitchen"]
    )
    markup.row(btnkitchen)
    btnbar = types.InlineKeyboardButton(
        f'Дати по буфету {emoji["wine"]}', url=web["bar"]
    )
    btnhookah = types.InlineKeyboardButton(
        f'КОЛЯНИ {emoji["dashing"]} ', url=web["hookah"]
    )
    markup.row(btnbar, btnhookah)
    bot.send_message(message.chat.id, "Меню", reply_markup=markup)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(
    func=lambda message: message.text == f'Виклик офіціанта {emoji["person_tiping"]}'
)
@colldown_decorator
@start_time
def callo(message):
    CDKEYBORDS[message.chat.id] = datetime.now()

    if USER.get(message.chat.id) == "/start":
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ',
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])

    elif USER.get(message.chat.id) is not None:
        bot.send_message(CHANNEL_ID, f"Офіціанта за  {USER.get(message.chat.id)}")
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'Вже біжить як дикий вепр {emoji["snail"]}')
        bot.send_sticker(message.chat.id, sticker=stickers[3])
    else:
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ',
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])


@bot.message_handler(
    func=lambda message: message.text == f'Виклик кальянщика {emoji["dashing"]}'
)
@colldown_decorator
@start_time
def callh(message):
    CDKEYBORDS[message.chat.id] = datetime.now()

    if USER.get(message.chat.id) == "/start":
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ',
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])

    elif USER.get(message.chat.id) is not None:
        bot.send_message(CHANNEL_ID, f"Кальянщика за  {USER.get(message.chat.id)}")
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'Вже мчить кабанчиком {emoji["boar"]}')
        bot.send_sticker(message.chat.id, sticker=stickers[6])

    else:
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ',
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])


@bot.message_handler(func=lambda message: message.text.startswith("Рахунок"))
@throttle
@start_time
def account(message):
    if USER.get(message.chat.id) == "/start":

        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ',
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])

    elif USER.get(message.chat.id) is not None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cash = types.KeyboardButton(f'Готівка {emoji["money_wings"]}')
        cart = types.KeyboardButton(f'Карта {emoji["card"]}')
        markup.row(cash, cart)
        bot.send_message(message.chat.id, "Оберіть метод оплати ", reply_markup=markup)
        bot.send_sticker(message.chat.id, sticker=stickers[4])
        bot.delete_message(message.chat.id, message.message_id)
        bot.register_next_step_handler(message, check)
    else:
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ',
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])


@bot.message_handler(commands=["check"])
@throttle
@start_time
def check(message):
    if message.text.startswith("Готівка"):
        bot.send_message(CHANNEL_ID, f"Рахунок готівкою за {USER.get(message.chat.id)}")

    elif message.text.startswith("Карта"):
        bot.send_message(CHANNEL_ID, f"Рахунок картою {USER.get(message.chat.id)}")

    bot.delete_message(message.chat.id, message.message_id)

    bot.send_message(message.chat.id, f'Вже друкуємо {emoji["memo"]}')
    bot.send_message(
        message.chat.id,
        f'До зустрічі я буду чекати на тебе {emoji["beating_hearth"]}',
        reply_markup=markupp,
    )
    bot.send_sticker(message.chat.id, sticker=stickers[5])


@bot.message_handler(func=lambda message: message.text == f'Відгук {emoji["speech"]}')
@throttle
@start_time
def response(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(f'Тиць{emoji["paw"]} ', url=web["feedback_google"])
    )
    bot.send_message(
        message.chat.id, f'Відгук{emoji["orange_hearth"]}', reply_markup=markup
    )
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(
    func=lambda message: message.text == f'Оцінити обслуговування {emoji.get("heart")}'
)
@throttle
@start_time
def tip(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(
        message.chat.id,
        f'Наші фокси завжди страються заради вашого комфорту {emoji["beating_hearth"]}',
        reply_markup=reyting_markup,
    )
    bot.send_message(CHANNEL_ID, f"{USER.get(message.chat.id)} столик")


@bot.message_handler(func=lambda message: message.text == f'Акції {emoji.get("fire")}')
@throttle 
@start_time
def take_action_for_users(message):
    with db:
        act = Actions.select().first()
        if not act:
            bot.send_message(message.chat.id, f'Зараз акцій немає {emoji.get("heart")}')
        for actions in Actions.select():
            try:
                with open(
                    os.path.join(path, f"{actions.image_data}.jpg"), "rb"
                ) as photo:
                    bot.send_photo(
                        message.chat.id, photo, caption=f"{actions.text_action}\n"
                    )
            except FileNotFoundError:
                bot.send_message(message.chat.id, f"{actions.text_action}\n")

        db.close()


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True)
        except Exception as e:
            time.sleep(3)
