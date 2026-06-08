# AI Telegram Assistant

Telegram-бот с AI-ответами, памятью диалога, PostgreSQL-базой данных и деплоем на Railway.

## Что это

Это MVP Telegram AI-ассистента.

Бот умеет принимать сообщения пользователя, отправлять их в AI-модель через OpenRouter, сохранять историю диалога в PostgreSQL и использовать последние сообщения как контекст для следующих ответов.

## Основные возможности

- AI-ответы через OpenRouter;
- память последних сообщений;
- сохранение истории в PostgreSQL;
- роли сообщений: `user` и `assistant`;
- очистка истории командой `/clear_messages`;
- просмотр последних сообщений через `/db_messages`;
- деплой на Railway;
- работа без включённого компьютера;
- настройка через переменные окружения.

## Как работает AI-flow

```txt
Пользователь пишет сообщение
↓
Telegram отправляет update
↓
бот достаёт последние сообщения из PostgreSQL
↓
бот отправляет историю + новое сообщение в OpenRouter
↓
AI возвращает ответ
↓
бот сохраняет сообщение пользователя
↓
бот сохраняет ответ ассистента
↓
бот отправляет ответ пользователю
```

## Технологии

- Python
- python-telegram-bot
- PostgreSQL
- psycopg2
- OpenRouter API
- Railway
- Git / GitHub
- python-dotenv

## Структура проекта

```txt
tg-minimal-bot/
├── ai_service.py
├── config.py
├── database.py
├── handlers.py
├── keyboards.py
├── main.py
├── renderers.py
├── requirements.txt
├── states.py
└── README.md
```

## Переменные окружения

Локально нужно создать `.env`, а на Railway добавить эти переменные в Variables:

```env
BOT_TOKEN=
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openai/gpt-4o-mini
DATABASE_URL=
AI_HISTORY_LIMIT=10
AI_TEMPERATURE=0.5
AI_MAX_TOKENS=500
```

## Запуск локально

1. Клонировать репозиторий:

```bash
git clone https://github.com/EzraMillerAi/tg-minimal-bot.git
cd tg-minimal-bot
```

2. Создать виртуальное окружение:

```bash
python -m venv .venv
```

3. Активировать окружение на Windows:

```bash
.venv\Scripts\activate
```

4. Установить зависимости:

```bash
pip install -r requirements.txt
```

5. Создать `.env` и заполнить переменные.

6. Запустить бота:

```bash
python main.py
```

## Команды

```txt
/start - запуск бота
/help - список команд
/profile - профиль пользователя
/db_messages - последние сохранённые сообщения
/db_messages_count - количество сообщений
/clear_messages - очистить историю сообщений
/db_settings - показать настройки
```

## Демо-сценарий

```txt
User: /clear_messages
Bot: История сообщений очищена.

User: меня зовут Влад
Bot: Приятно познакомиться, Влад! Как я могу помочь?

User: как меня зовут?
Bot: Тебя зовут Влад.
```

Этот сценарий показывает, что бот использует историю сообщений как контекст для AI-ответов.

## Текущий статус

MVP-версия.

Уже реализовано:

- AI-ответы;
- память диалога;
- PostgreSQL-хранилище;
- деплой на Railway;
- настройка через `.env`;
- сохранение истории сообщений.

## Возможные улучшения

- улучшенная обработка ошибок;
- более чистое разделение dev-команд и user-команд;
- кастомные промпты под бизнес;
- FAQ-режим;
- база знаний;
- шаблон под клиентские Telegram-боты.