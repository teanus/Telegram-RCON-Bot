
# TeaRCON

Telegram RCON bot для игры Minecraft Bedrock и Java edition




## Установка

Установите зависимости для работы

```bash
  cd telegram-rcon-bot
  pip install -r requirements.txt

```

## Настройка

Создайте файл без имени с расширением .env, как показано на фото:

![File env](https://imgur.com/iO9Fuql.png)

Заполните его поля данными:

    TOKEN= Токен вашего бота телеграмм полученный от BotFather
    rcon_host= ip_address вашего сервера, если бот установлен с сервером на одном сервере, то 127.0.0.1
    rcon_port = Порт вашего rcon, можно узнать в файле server.properties
    rcon_password = Пароль от вашего rcon, можно узнать в файле server.properties

## Выдача прав администратора

📢ВАЖНО! В config.json должен стоять True в поле: 

    "console": {
         "give_role": true
    }
      
Для первой выдачи прав администратора нужно получить user id, перезапустить бота и в консоли при запросе ввести или вставить id: <br>

![Give admin](https://imgur.com/KzT05IN.png)

В дальнейшем администратор может напрямую добавлять других пользователей, напрямую через админ-панель бота

##  Использование PostgreSQL

Если вы используете бд PostgreSQL, то вам нужно дополнительно дозаполнить файл env

    postgre_host= ip_address где расположена бд
    postgre_port= port вашего postgresql
    postgre_database_name= Название бд выделенной под бота
    postgre_username= Пользователь вашей бд обладающей правами доступа
    postgre_password= Пароль от вашего пользователя


## Запуск

Запуск рекомендуется делать при использовании мультиплексора tmux или его аналогов

Установка **tmux**

```bash
  apt install tmux
```
Команды запуска

```bash
  tmux new -s tearcon 
  python3 bot.py 
```


## Особенности

- Администрирование бота прямо из него
- Полный контроль над пользователями
- Черный список команд
- Ассинхронная работа
- Скорость обслуживания
- Использование передовых баз данных
- PostgeSQL или SQLite3 - все для души
- Грамотная постановка запросов к БД и внесение изменений
- Логирование бота напрямую в беседу
  
    - Логирование имеет ограничение на размер файла (по умолчанию 5мбайт)
    - Логирование имеет автоматические бэкап файлы (по умолчанию 2)


## Планы на будущее

- [ ] Сделать возможность кастомизации сообщений вне кода

- [ ] Написать свой ассинхронный интерфейс RCON
      
✅ Кастомизация команд и клавиатуры
<br>
✅ Полноценное логирование
<br>
❌ Перестать лениться :)

## 🔗 Связаться
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/teanus)
[![Вконтакте](https://img.shields.io/badge/вконтакте-%232E87FB.svg?&style=for-the-badge&logo=vk&logoColor=white
)](https://vk.com/dimawinchester)


## Лицензия


[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)


