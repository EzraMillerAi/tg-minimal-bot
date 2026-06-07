from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="About", callback_data="about_button"),
            InlineKeyboardButton(text="Ping", callback_data="ping_button"),
            InlineKeyboardButton(text="Profile", callback_data="profile_button"),
            InlineKeyboardButton(text="Settings", callback_data="settings_button"),
            InlineKeyboardButton(text="Set Name", callback_data="set_name_button"),
            InlineKeyboardButton(text="Set Age", callback_data="set_age_button"),
            InlineKeyboardButton(text="Set City", callback_data="set_city_button"),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="Back", callback_data="back_to_menu"),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

def get_success_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                text="Main Menu",
                callback_data="back_to_menu",
            ),

            InlineKeyboardButton(
                text="Profile",
                callback_data="profile_button",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_settings_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                text="Toggle Notifications",
                callback_data="toggle_notifications",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Toggle Theme",
                callback_data="toggle_theme",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Back",
                callback_data="back_to_menu",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)