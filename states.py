from renderers import (
    render_main_menu,
    render_about_screen,
    render_ping_screen,
    render_profile_screen,
    render_settings_screen,
    render_set_name_screen,
    render_set_age_screen,
    render_set_city_screen,
)

NAVIGATION_MAP = {
    "about_button": "about",
    "ping_button": "ping",
    "back_to_menu": "main_menu",
    "profile_button": "profile",
    "settings_button": "settings",
    "set_name_button": "waiting_for_name",
    "set_age_button": "waiting_for_age",
    "set_city_button": "waiting_for_city",
    "toggle_notifications": "settings",
    "toggle_theme": "settings",
}

INPUT_STATES = {
    "waiting_for_name": {
        "field": "name",
        "success_message": "Имя сохранено",
    },

    "waiting_for_age": {
        "field": "age",
        "success_message": "Возраст сохранён",
        "validator": "number",
    },

    "waiting_for_city": {
        "field": "city",
        "success_message": "Город сохранён",
    },
}

SCREEN_RENDERERS = {
    "about": render_about_screen,
    "ping": render_ping_screen,
    "main_menu": render_main_menu,
    "profile": render_profile_screen,
    "settings": render_settings_screen,
    "waiting_for_name": render_set_name_screen,
    "waiting_for_age": render_set_age_screen,
    "waiting_for_city": render_set_city_screen,
}