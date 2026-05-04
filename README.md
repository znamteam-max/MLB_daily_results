# MLB Daily Results Telegram Bot

Бот публикует ежедневный общий пост с результатами MLB в закрытый канал
`-1003643946438` и умеет править русские названия/фамилии через команды.

## Быстрый старт

1. Создайте `.env` по примеру `.env.example`.
2. Добавьте `@mlb_daily_results_bot` администратором канала с правом публиковать и редактировать сообщения.
3. Установите зависимости:

```powershell
pip install -r requirements.txt
```

4. Запустите бота:

```powershell
python mlb_daily_results_bot.py
```

При запуске long polling бот по умолчанию снимает старый Telegram webhook
(`DELETE_WEBHOOK_ON_START=true`), иначе Telegram может не отдавать апдейты.

## Команды

`/today [YYYY-MM-DD]` - показать пост результатов.

`/schedule [YYYY-MM-DD]` - расписание дня с количеством матчей и временем МСК.

`/status [YYYY-MM-DD]` - сколько матчей завершено и опубликован ли пост.

`/post [YYYY-MM-DD]` - отправить пост в канал или обновить уже отправленный.

`/refresh [YYYY-MM-DD]` - перегенерировать и отредактировать уже опубликованный пост.

`/fix English Name = Русское Имя` - запомнить перевод имени/фамилии игрока.

`/team Twins = Твинс` - запомнить название команды.

`/replace старый текст = новый текст` - заменить текст в последнем опубликованном посте.

`/dict [поиск]` - показать сохранённые правки.

`/unknown [YYYY-MM-DD]` - показать имена игроков за день, которых ещё нет в словаре.

## Автопостинг

При `AUTO_POST=true` бот каждые `AUTO_CHECK_SECONDS` секунд проверяет последние
`AUTO_LOOKBACK_DAYS` игровых дней MLB. Как только все матчи дня финальные,
он публикует пост. Повторной публикации за ту же дату не будет: `message_id`
сохраняется в SQLite.

## Деплой: постоянный worker

Проект можно запускать как постоянный worker-процесс. Для PaaS есть `Procfile`,
для контейнера - `Dockerfile`. Важно сохранить `state/` между перезапусками,
иначе бот не будет помнить уже опубликованные `message_id` и словарь правок.

## Деплой: Vercel + cron-jobs.org

Vercel не запускает бесконечный polling-процесс. Для Vercel используются HTTP
functions:

`/api/telegram` - Telegram webhook для команд.

`/api/cron?secret=...` - проверка результатов и автопостинг.

`/api/health` - быстрая проверка переменных окружения.

На Vercel нужно добавить переменные:

```env
TELEGRAM_BOT_TOKEN=...
TARGET_CHAT_ID=-1003643946438
CRON_SECRET=длинная_случайная_строка
KV_URL=...
FAST_PITCHER_RECORDS=true
```

`KV_URL` или `REDIS_URL` обязателен на Vercel: файловая система serverless
функций не хранит SQLite между вызовами. Подойдёт Vercel KV / Upstash Redis.
`FAST_PITCHER_RECORDS=true` берёт рекорды питчеров пачкой и держит cron-функцию
короткой для serverless-лимитов.

После деплоя задайте Telegram webhook:

```text
https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=https://<your-project>.vercel.app/api/telegram
```

В cron-jobs.org создайте задачу каждую минуту:

```text
https://<your-project>.vercel.app/api/cron?secret=<CRON_SECRET>
```

Для ручной проверки конкретной даты:

```text
https://<your-project>.vercel.app/api/cron?secret=<CRON_SECRET>&date=2026-05-03
```

Для проверки без Telegram:

```powershell
python mlb_daily_results_bot.py --date 2026-05-03 --dry-run
python mlb_daily_results_bot.py --schedule --date 2026-05-03 --dry-run
```
