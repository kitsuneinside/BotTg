from decorators import bot
from DB import Message, path, User, db
import os
import random
import string
from datetime import datetime
from Markup import adminmarkupp, adminmarkupp2, edit_markup
from telebot.apihelper import ApiTelegramException
import time


def safe_send(chat_id, text, photo_path=None):
    try:
        if photo_path and os.path.exists(photo_path):
            with open(photo_path, "rb") as photo:
                bot.send_photo(chat_id, photo, caption=text)
        else:
            bot.send_message(chat_id, text)

    except ApiTelegramException:
        print(f"SKIP {chat_id}: blocked or chat not found")

    except Exception as e:
        print(f"ERROR {chat_id}: {e}")


def name_generation(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


@bot.message_handler(commands=["planed_message_bar"])
def planed_message_barr(message):
    bot.send_message(
        message.chat.id, "Обери що бажаєш редагувати", reply_markup=adminmarkupp
    )


@bot.message_handler(commands=["action_bar"])
def action_barr(message):
    bot.send_message(
        message.chat.id, "Обери що бажаєш редагувати", reply_markup=adminmarkupp2
    )


@bot.message_handler(commands=["send_messages_from_users"])
def send_name_event(message):
    bot.send_message(
        message.chat.id,
        "Надішліть назву запланованого повідомлення яке має бути відправлене ",
    )
    bot.register_next_step_handler(message, send_messages)


def send_messages(message):
    mess = Message.get_or_none(Message.name == message.text)

    if not mess:
        bot.send_message(message.chat.id, "Повідомлення з такою назвою не знайдено")
        return

    textt = mess.text_message
    file_path = mess.image_data

    photo_path = None
    if file_path and file_path != "DEFAULT":
        photo_path = os.path.join(path, f"{file_path}.jpg")

    for user in User.select():
        print("SEND TO:", user.chat_id)
        safe_send(user.chat_id, textt, photo_path)
        time.sleep(0.05)
    bot.send_message(message.chat.id, "Доставлено")


@bot.message_handler(commands=["event_list"])
def select_all_from_db(message):
    with db:
        mess = Message.select().first()
        if not mess:
            bot.send_message(message.chat.id, "Повідомлень немає")
            return
        else:
            for mess in Message.select():
                try:
                    with open(
                        os.path.join(path, f"{mess.image_data}.jpg"), "rb"
                    ) as photo:
                        bot.send_photo(
                            message.chat.id,
                            photo,
                            caption=f"name: {mess.name}\n"
                            f"text: {mess.text_message}\n"
                            f"date: {mess.date}\n",
                        )
                except FileNotFoundError:
                    bot.send_message(
                        message.chat.id,
                        f"name: {mess.name}\n"
                        f"text: {mess.text_message}\n"
                        f"date: {mess.date}\n",
                    )


@bot.message_handler(commands=["add_events"])
def tmp(message):
    bot.send_message(message.chat.id, "Надішліть назву для запланованого повідомлення")
    bot.register_next_step_handler(message, insert_photo_in_db)


def insert_photo_in_db(message):
    event_name = message.text
    bot.send_message(
        message.chat.id,
        "Надішліть фото для запланованого повідомлення, або відправте будь-який текст, "
        "щоб пропустити цей крок",
    )
    bot.register_next_step_handler(message, download_image, event_name)


def download_image(message, event_name):
    if message.photo:

        fileid = message.photo[-1].file_id
        file_info = bot.get_file(fileid)
        downloaded_file = bot.download_file(file_info.file_path)
        event_photo = f"{name_generation()}"

        with open(os.path.join(path, f"{event_photo}.jpg"), "wb") as new_file:
            new_file.write(downloaded_file)

        bot.register_next_step_handler(message, insert_in_db, event_name, event_photo)
        bot.send_message(
            message.chat.id, "Надішліть текст для запланованого повідомлення"
        )

    else:
        bot.register_next_step_handler(message, insert_in_db, event_name)
        bot.send_message(
            message.chat.id, "Надішліть текст для запланованого повідомлення"
        )


def insert_in_db(message, event_name, event_photo="DEFAULT"):
    try:
        db.connect(reuse_if_open=True)

        Message.create(
            name=event_name,
            text_message=message.text or "",
            date=datetime.now(),
            image_data=event_photo,
        )

        bot.send_message(
            message.chat.id, "Заплановане повідомлення добавлене в базу даних"
        )

    except Exception as e:
        print("ERROR:", repr(e))

    finally:
        if not db.is_closed():
            db.close()


@bot.message_handler(commands=["edit_event"])
def chose_edit(message):
    bot.send_message(
        message.chat.id, "Обери що бажаєш змінити", reply_markup=edit_markup
    )


@bot.message_handler(commands=["edit_text"])
def name_edit_t(message):
    bot.register_next_step_handler(message, edit_t)
    bot.send_message(
        message.chat.id, "Надішліть назву повідомлення в якому бажаєте замінти текст"
    )


def edit_t(message):
    with db.atomic():
        message_record = Message.get_or_none(Message.name == message.text)
        if not message_record:
            bot.send_message(
                message.chat.id, f"Подія з назвою '{message.text}' не знайдена."
            )
            return
        bot.send_message(
            message.chat.id, f"Текст який є зараз: {message_record.text_message}"
        )
        bot.register_next_step_handler(
            message, lambda m: insert_edit_txt(m, message_record)
        )


def insert_edit_txt(message, db_record):
    with db.atomic():
        db_record.text_message = message.text
        db_record.save()
    bot.send_message(message.chat.id, "Текст оновлено успішно!")


@bot.message_handler(commands=["edit_photos"])
def name_edit_p(message):
    bot.register_next_step_handler(message, edit_photo)
    bot.send_message(
        message.chat.id, "Надішліть назву повідомлення в якому бажаєте замінти фото"
    )


def edit_photo(message):
    try:
        with db.atomic():
            photo_name = Message.get_or_none(Message.name == message.text)
            if not photo_name:
                bot.send_message(message.chat.id, "Такого повідомлення немає")
                return
            if photo_name.image_data == "DEFAULT":
                bot.register_next_step_handler(
                    message, lambda m: download_for_edit_image(m, photo_name.image_data)
                )
                bot.send_message(
                    message.chat.id, "Надішліть фото на яке бажаєте замінити"
                )

            else:
                with open(
                        os.path.join(path, f"{photo_name.image_data}.jpg"), "rb"
                ) as photo:
                    bot.send_photo(message.chat.id, photo)
                    bot.send_message(
                        message.chat.id,
                        "Фото яке використовується на даний момент",
                    )
                    bot.register_next_step_handler(
                        message,
                        lambda m: download_for_edit_image(m, photo_name.image_data),
                    )
                    bot.send_message(
                        message.chat.id,
                        "Надішліть фото на яке бажаєте замінити",
                    )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id, f"фото з назвою '{message.text}' не знайдена."
        )


def download_for_edit_image(message, event_name):
    if message.photo:
        if not os.path.exists(path):
            os.makedirs(path)

        fileid = message.photo[-1].file_id
        file_info = bot.get_file(fileid)
        downloaded_file = bot.download_file(file_info.file_path)
        event_photo = f"{name_generation()}"

        with open(os.path.join(path, f"{event_photo}.jpg"), "wb") as new_file:
            new_file.write(downloaded_file)
        with db.atomic():
            for mess in Message:
                if mess.image_data == event_name:
                    mess.image_data = f"{event_photo}"
                    mess.save()
    bot.send_message(message.chat.id, "Фото змінено")


@bot.message_handler(commands=["delete_event"])
def take_name(message):
    bot.send_message(message.chat.id, "Надішліть назву запланованого повідомлення")
    bot.register_next_step_handler(message, delete_from_db)


def delete_from_db(message):
    with db:
        mess = Message.get_or_none(Message.name == message.text)
        if not mess:
            bot.send_message(message.chat.id, "Повідомлення з такою назвою немає")
            return
        else:
            for mes in Message.select():
                if mes.name == message.text:
                    mes.delete_instance()
                    bot.send_message(message.chat.id, "Повідомлення видалене")
