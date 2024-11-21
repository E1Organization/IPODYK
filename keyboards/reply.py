from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🖥️ Добавить товар"),
            KeyboardButton(text="🗒️ Просмотреть отслеживаемые товары"),
            KeyboardButton(text="✂️ Удалить товар")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите действие из меню...",
    selective=True
)


rmk = ReplyKeyboardRemove()