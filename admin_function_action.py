from admin_function_message import name_generation
from bot_info import bot
from DB import path, db, Actions
from Markup import edit_action_markup
from datetime import datetime
import os


@bot.message_handler(commands=["add_action"])
def add_action_(message):
    bot.send_message(message.chat.id, "Надішліть назву акції")
    bot.register_next_step_handler(message, insert_photo_in_db_action)


def insert_photo_in_db_action(message):
    event_name = message.text
    bot.send_message(
        message.chat.id,
        "Надішліть фото для акції, або відправте будь-який текст, "
        "щоб пропустити цей крок",
    )
    bot.register_next_step_handler(message, download_image_for_action, event_name)


def download_image_for_action(message, action_name):
    if message.photo:

        fileid = message.photo[-1].file_id
        file_info = bot.get_file(fileid)
        downloaded_file = bot.download_file(file_info.file_path)
        action_photo = f"{name_generation()}"

        with open(os.path.join(path, f"{action_photo}.jpg"), "wb") as new_file:
            new_file.write(downloaded_file)

        bot.register_next_step_handler(
            message, insert_action_in_db, action_name, action_photo
        )
        bot.send_message(message.chat.id, "Надішліть текст для акції")
    else:
        bot.register_next_step_handler(message, insert_action_in_db, action_name)
        bot.send_message(message.chat.id, "Надішліть текст для акції")


def insert_action_in_db(message, action_name, action_photo="DEFAULT"):
    with db:
        Actions.create(
            name=f"{action_name}",
            text_action=message.text,
            date=datetime.now(),
            image_data=f"{action_photo}",
        )
        bot.send_message(message.chat.id, "Акція добавлена в базу даних")


@bot.message_handler(commands=["action_list"])
def select_all_action_from_db(message):
    with db:
        act = Actions.select().first()
        if not act:
            bot.send_message(message.chat.id, "Зараз акцій немає")
            return
        for mess in Actions.select():
            if mess.image_data == 'DEFAULT':
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"name: {mess.name}\n"
                            f"text: {mess.text_action}\n"
                            f"date: {mess.date}\n",
                )
            else:
                try:
                    with open(
                            os.path.join(path, f"{mess.image_data}.jpg"), "rb"
                    ) as photo:
                        bot.send_photo(
                            message.chat.id,
                            photo,
                            caption=f"name: {mess.name}\n"
                                    f"text: {mess.text_action}\n"
                                    f"date: {mess.date}\n",
                        )
                except FileNotFoundError:
                    bot.send_message(
                        message.chat.id,
                        f"name: {mess.name}\n"
                        f"text: {mess.text_action}\n"
                        f"date: {mess.date}\n",
                    )


@bot.message_handler(commands=["delete_action"])
def take_name_action_(message):
    bot.send_message(message.chat.id, "Надішліть назву акції")
    bot.register_next_step_handler(message, delete_action_from_db)


def delete_action_from_db(message):
    with db:
        act = Actions.get_or_none(Actions.name == message.text)
        if not act:
            bot.send_message(message.chat.id, "Такої акції немає")
            return
        else:
            for mes in Actions.select():
                if mes.name == message.text:
                    mes.delete_instance()
                    bot.send_message(message.chat.id, "Ація видалена")


@bot.message_handler(commands=["edit_action"])
def chose_action_for_edit(message):
    bot.send_message(
        message.chat.id, "Обери що бажаєш змінити", reply_markup=edit_action_markup
    )


@bot.message_handler(commands=["edit_text_action"])
def name_edit_t_action(message):
    bot.register_next_step_handler(message, edit_t_in_action)
    bot.send_message(
        message.chat.id, "Надішліть назву акції в якій бажаєте замінти текст"
    )


def edit_t_in_action(message):
    with db.atomic():
        message_record = Actions.get_or_none(Actions.name == message.text)
        if not message_record:
            bot.send_message(
                message.chat.id, f"Подія з назвою '{message.text}' не знайдена."
            )
            return
        bot.send_message(
            message.chat.id, f"Текст який є зараз: {message_record.text_action}"
        )
        bot.register_next_step_handler(
            message, lambda m: insert_edit_txt_in_action(m, message_record)
        )


def insert_edit_txt_in_action(message, db_record):
    with db.atomic():
        db_record.text_action = message.text
        db_record.save()
    bot.send_message(message.chat.id, "Текст оновлено успішно!")


@bot.message_handler(commands=["edit_photos_action"])
def name_edit_p_in_action(message):
    bot.register_next_step_handler(message, edit_photo_action)
    bot.send_message(
        message.chat.id, "Надішліть назву акції в якій бажаєте замінти фото"
    )


def edit_photo_action(message):
    try:
        with db.atomic():
            photo_name = Actions.get_or_none(Actions.name == message.text)
            if not photo_name:
                bot.send_message(message.chat.id, "Такої акції немає")
                return
            if photo_name.image_data == "DEFAULT":
                bot.register_next_step_handler(
                    message,
                    lambda m: download_for_edit_image_action(m, photo_name.image_data),
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
                        lambda m: download_for_edit_image_action(m, photo_name.image_data),
                    )
                    bot.send_message(
                        message.chat.id,
                        "Надішліть фото на яке бажаєте замінити",
                    )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id, f"фото з назвою '{message.text}' не знайдена."
        )


def download_for_edit_image_action(message, event_name):
    if message.photo:

        fileid = message.photo[-1].file_id
        file_info = bot.get_file(fileid)
        downloaded_file = bot.download_file(file_info.file_path)
        event_photo = f"{name_generation()}"

        with open(os.path.join(path, f"{event_photo}.jpg"), "wb") as new_file:
            new_file.write(downloaded_file)
        with db.atomic():
            for mess in Actions:
                if mess.image_data == event_name:
                    mess.image_data = f"{event_photo}"
                    mess.save()

    bot.send_message(message.chat.id, "Фото змінено")
