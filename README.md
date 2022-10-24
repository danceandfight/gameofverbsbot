# Боты для общения с пользователями Telegram и VK

Обучаемые боты, которые умеют общаться с пользователями, используя возможности нейросети DialogFlow.

![](https://raw.githubusercontent.com/danceandfight/gameofverbsbot/main/tg.gif)

Поболтать с ботом можно в [чате в VK](https://vk.com/club216618579) или в [телеграме](https://t.me/dvmnxxhelpergov_bot)

## Как установить

**Важно!** Предварительно должен быть установлен python версии не выше 3.9.x.

Скачайте код:
```sh
git clone git@github.com:danceandfight/gameofverbsbot.git
```

Перейдите в каталог проекта:
```sh
cd gameofverbsbot
```
Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии. 

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`

Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Зарегестрируйте нового бота с помощью `@BotFather` в телеграме. Вам потребуется его токен, который выдаст `@BotFather` после регистрации.

Создайте новую группу в [VK](vk.com) и получите токен группы в меню `Настройки/Работа с API`.

Зарегистрируйтесь на [dialogflow](https://dialogflow.cloud.google.com/#/login) и создайте там проект выбрав `new project`. Вам потребуется `Project ID` из вкладки `Project Info` в `Dashboard`.

Создайте [агента](https://cloud.google.com/dialogflow/docs/quick/build-agent) используя `Project ID` и обязательно выберите русский язык.

Создайте `.json` [ключ](https://cloud.google.com/docs/authentication/getting-started) для `GOOGLE_APPLICATION_CREDENTIALS`.

Создайте файл `.env` в каталоге `gameofverbsbot/` и положите туда код такого вида, заменив токены на свои:
```sh
TELEGRAM_BOT_TOKEN=1234546789:ASFGRrogjRHrtweog-bRTHrhwmniireeoWW
GOOGLE_APPLICATION_CREDENTIALS=</Путь/до/файла/.json>
GOOGLE_PROJECT_ID=<Project ID>
LANGUAGE_CODE='ru'
VK_TOKEN='vk1.a.qokPsGegrJtr...'
```

Запустите telegram бота:

```sh
python tg_bot.py
```
Запустите vk бота:

```sh
python vk_bot.py
```

## Как пользоваться

Можно натренировать DialogFlow вручную в меню `Intents`, выбирая варианты вопросов от пользователя в `Training phrases` и ответы бота в `Text responses`.
Можно воспользоваться готовыми тестовыми данными из файла questions использовав команду:
```sh
python teach_dialogflow.py
```

Начните диалоги с двумя вашими ботами.

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).