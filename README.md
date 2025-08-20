# sigmax

(Недоделанная) Python-библиотека для работы с польовательским API мессенджера [MAX](https://max.ru/) (OneMe).

Да, оно работает. Да, я не знаю как.

Буду рад всем PRам.

## Установка

1. Перекреститесь.

2. `pip install git+https://github.com/moontr3/sigmax.git`

## Quick Start

Для начала нужно получить токен от вашего аккаунта. Пока это можно сделать залогинившись в [веб-версии MAX](https://web.max.ru) и полазив по кукисам, либо в той же браузерной версии отследить, какой токен отправляет приложение через Websocket.

Для примера возьмём код, который будет отвечать словом "Привет" на любое ваше сообщение, начинающиеся с точки (`.`).

```py
import asyncio
import sigmax

client = sigmax.Client()

@client.on_message()
async def on_message(message: sigmax.Message):
    if message.sender_id != client.me.id: return
    
    if message.text.startswith('.'):
        message = await client.send_message(
            message.chat_id, 'Привет!', reply_to=message.id
        )
        
asyncio.run(client.login_with_token("ТОКЕН"))
```

Для получения списка чатов, где вы состоите, можно использовать функцию `client.get_chats()`.

```py
async for chat in client.get_chats():
    print(chat.title)
```

Для получения чатов по их ID, можно использовать `client.get_chat_by_id()`.

```py
chats = await client.get_chats_by_id([123, 456, 789])
for i in chats:
    print(i.title)

# или

chat = await client.get_chats_by_id([123])[0]
print(chat.title)
```

Для получения пользователя по номеру телефона, можно использовать `client.get_user_by_phone()`.

```py
user = await client.get_user_by_phone('+78005553535')
print(user.name)
```

## Прочее

~~Если~~ Когда возникнут вопросы, можно связаться со мной в одном [чате разработчиков](https://max.ru/join/xzUCRiPjt_G7EaLtKLe7PgT69GPRP51BHHEv7n5W7J0) в Максе или в [ТГ](https://t.me/moontr3) тоже можно да.

Кстати список опкодов можно найти [тут](sigmax/opcodes.py).

## Ту-ту (хаха типа поняли шутка ту-ду но паровозик туту поняли же да???? даа???????)

- [x] Получение и отправка сообщений
- [x] Получение списка чатов
- [ ] **Починить отключение через пару минут после инициализации вебсокета**
- [ ] Начать писать документацию
- [ ] Действия в чатах (администрирование, списки участников, настройки)
- [ ] Получение информации о пользователях
- [ ] Загрузка файлов и отправка вложений
- [ ] Логин по номеру телефона
- [ ] Форматирование текста
- [ ] Нормальная обработка ошибок
- [ ] Допройти курс "Asyncio для начинающих"
- [ ] Ну и так по мелочи