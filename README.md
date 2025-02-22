# Запуск проекта

1. Клонируйте репозиторий:

```
git clone https://github.com/iMaanick/HoroscopeBot.git
```

2. При необходимости установить Poetry ```pip install poetry```

3. Запустить виртуальное окружение ```poetry shell```

4. Установить зависимости ```poetry install```


5. Добавьте файл .env и заполните его как в примере .example.env, используйте sqlite =):

```
TOKEN=BOT_TOKEN
DATABASE_URI=sqlite+aiosqlite:///test.db
```
6. Выполнить для создания таблиц

```
alembic upgrade head 
```

7. Для запуска выполните:
```
python -m app.main
```

# Функциональность

1. При регистрации бот предлагает пользователю выбрать свой знак зодиака. После выбора знака бот присылает сообщение с информацией о выбранном знаке
2. После регистрации бот присылает гороскоп на сегодня с картинкой и кнопкой `Обновить`
3. Каждый день в 10 утра пользователь получает гороскоп на новый день (только в случае, если его еще нет)
4. В меню бота есть команда `/update`, которая обновляет прогноз на сегодня (аналогично кнопке `Обновить` в сообщении) либо отправляет новое сообщение с гороскопом, если сообщения за сегодня по какой-то причине нет
5. Когда пользователь отправляет что-либо в чат, бот пишет `Извините, я не понял`
6. В меню бота есть команда `/change_zodiac`. При нажатии появляется клавиатура, и знак зодиака пользователя меняется на выбранный. Приходит новый гороскоп на сегодня
7. В меню бота есть команда `/clear_history`, которая очищает историю сообщений, оставляя только сообщение с последним выбранным знаком зодиака


# О проекте
1. SQLAlchemy для работы с базой данных, sqlite в качестве базы данных
2. Alembic для управления миграциями
3. Aiogram и aiogram-dialog для работы с telegram bot api
4. Apscheduler для периодических заданий
5. Poetry для управления зависимостями
