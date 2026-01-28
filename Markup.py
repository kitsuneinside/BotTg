from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from telebot import types

from sticker import emoji

markupp = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton(f'Меню {emoji.get("fork_knife")}')
btn5 = KeyboardButton(f'Рахунок {emoji.get("page")}')
markupp.row(btn1, btn5)
btn2 = KeyboardButton(f'ВDідгук {emoji.get("speech")}')
btn3 = KeyboardButton(f'Виклик офіціанта {emoji.get("person_tiping")}')
btn4 = KeyboardButton(f'Виклик кальянщика {emoji.get("dashing")}')
btn7 = KeyboardButton(f'Оцінити обслуговування {emoji.get("heart")}')
btn6 = KeyboardButton(f'Акції {emoji.get("fire")}')
markupp.row(btn2, btn3, btn4)
markupp.row(btn7, btn6)

# reyting buttom
reyting_markup = types.InlineKeyboardMarkup()
reyting1_markup = types.InlineKeyboardButton(
    text=f'{emoji.get("keycap1")}', callback_data="1"
)
reyting2_markup = types.InlineKeyboardButton(
    text=f'{emoji.get("keycap2")}', callback_data="2"
)
reyting3_markup = types.InlineKeyboardButton(
    text=f'{emoji.get("keycap3")}', callback_data="3"
)
reyting4_markup = types.InlineKeyboardButton(
    text=f'{emoji.get("keycap4")}', callback_data="4"
)
reyting5_markup = types.InlineKeyboardButton(
    text=f'{emoji.get("keycap5")}', callback_data="5"
)
reyting_markup.row(
    reyting1_markup, reyting2_markup, reyting3_markup, reyting4_markup, reyting5_markup
)


# admin panel
edit_menu_markup = types.InlineKeyboardMarkup()
edit_menu_action_butom = types.InlineKeyboardButton("Акції", callback_data="action_bar")
edit_menu_planed_butomc = types.InlineKeyboardButton(
    "Повідомлення", callback_data="planed_message_bar"
)
edit_menu_markup.row(edit_menu_planed_butomc, edit_menu_action_butom)

# planed message bar
adminmarkupp = types.InlineKeyboardMarkup()

event_list_botton = types.InlineKeyboardButton(
    f"Список повідомлень", callback_data="event_list"
)
send_messages_button = types.InlineKeyboardButton(
    f"Розсилка", callback_data="send_messages_from_users"
)
adminmarkupp.row(event_list_botton, send_messages_button)
add_events_button = types.InlineKeyboardButton(
    f"Добавити заплановане повідомлення", callback_data="add_events"
)
adminmarkupp.row(add_events_button)
delete_event_button = types.InlineKeyboardButton(
    f"Видалити заплановане повідомлення", callback_data="delete_event"
)
adminmarkupp.row(delete_event_button)
edit_event_button = types.InlineKeyboardButton(
    f"Редагувати", callback_data="edit_event"
)
adminmarkupp.row(edit_event_button)

# action bar
adminmarkupp2 = types.InlineKeyboardMarkup()

action_list_botton = types.InlineKeyboardButton(
    f"Список акцій", callback_data="action_list"
)
adminmarkupp2.row(action_list_botton)
add_action_button = types.InlineKeyboardButton(
    f"Добавити акцію", callback_data="add_action"
)
adminmarkupp2.row(add_action_button)
delete_action_button = types.InlineKeyboardButton(
    f"Видалити акцію", callback_data="delete_action"
)
adminmarkupp2.row(delete_action_button)
edit_action_button = types.InlineKeyboardButton(
    f"Редагувати", callback_data="edit_action"
)
adminmarkupp2.row(edit_action_button)


# planed message button
edit_markup = types.InlineKeyboardMarkup()
edit_text_botton = types.InlineKeyboardButton(
    f"Змінити текст", callback_data="edit_text"
)
edit_photo_botton = types.InlineKeyboardButton(
    f"Замінити фото", callback_data="edit_photos"
)
edit_markup.row(edit_text_botton, edit_photo_botton)


# action botton
edit_action_markup = types.InlineKeyboardMarkup()
edit_action_p = types.InlineKeyboardButton(
    "Замінити фото", callback_data="edit_photos_action"
)
edit_action_t = types.InlineKeyboardButton(
    "Змінити текст", callback_data="edit_text_action"
)
edit_action_markup.row(edit_action_p, edit_action_t)
