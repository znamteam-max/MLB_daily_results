# MLB Daily Results Bot на Cloudflare Workers

Бот публикует ежедневный общий пост с результатами MLB в закрытый Telegram-канал
`-1003643946438`, принимает команды через Telegram webhook и сам проверяет
результаты каждую минуту через Cloudflare Cron Triggers.

## Что внутри

`src/worker.js` - основной Cloudflare Worker.

`wrangler.toml` - конфигурация Worker, KV binding и cron `* * * * *`.

`.dev.vars.example` - пример локальных переменных.

Workers KV используется для памяти бота: уже опубликованные посты, `message_id`
и словарь правок имён/команд.

Cron каждую минуту обновляет меню в канале и публикует результаты в
`TARGET_CHAT_ID`, как только все матчи игрового дня завершены.

## Команды бота

`/today [YYYY-MM-DD]` - показать пост результатов.

`/schedule [YYYY-MM-DD]` - расписание дня и количество матчей.

`/status [YYYY-MM-DD]` - статус игрового дня.

`/post [YYYY-MM-DD]` - отправить или обновить пост в канале.

`/refresh [YYYY-MM-DD]` - перегенерировать опубликованный пост.

`/fix English Name = Русское Имя` - запомнить имя игрока.

`/team Twins = Твинс` - запомнить название команды.

`/replace старый текст = новый текст` - поправить последний пост.

`/dict [поиск]` - показать словарь правок.

`/unknown [YYYY-MM-DD]` - показать имена без ручной правки.

`/menu [YYYY-MM-DD]` - создать или обновить меню в целевом канале.

В канале бот держит отдельное меню-сообщение с кнопками дат. В меню видно:
сколько матчей всего, сколько сыграно, сколько идёт сейчас, сколько ожидает
старта и опубликованы ли результаты за выбранную дату.

После публикации под постом и в меню есть кнопка `✏️ Править фамилии`. Она
показывает подсказку для команды `/fix English Name = Русское Имя`. Правка
сохраняется в Workers KV и применяется ко всем будущим постам.

В итоговом посте жирным выделяются названия команд. Строка `Хоум-раны`
скрывается, если в матче не было хоум-ранов. Если игрок выбил 2+ хоумрана,
рядом добавляется `🔥`. Если победивший питчер сделал quality start, рядом
добавляется `🎯`.

## Локальная подготовка

```powershell
npm install
copy .dev.vars.example .dev.vars
```

В `.dev.vars` впишите:

```env
TELEGRAM_BOT_TOKEN=...
TARGET_CHAT_ID=-1003643946438
CRON_SECRET=длинная_случайная_строка
TELEGRAM_WEBHOOK_SECRET=длинная_случайная_строка
```

Локальный запуск:

```powershell
npm run dev
```

## Деплой на Cloudflare

1. Авторизуйтесь в Cloudflare:

```powershell
npx wrangler login
```

2. Создайте/привяжите KV namespace. В `wrangler.toml` binding уже называется
`MLB_STATE`. Современный Wrangler может создать KV автоматически при deploy.
Если попросит ID вручную:

```powershell
npx wrangler kv namespace create MLB_STATE
```

Затем вставьте выданный `id` в `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "MLB_STATE"
id = "..."
```

3. Задайте secrets:

```powershell
npx wrangler secret put TELEGRAM_BOT_TOKEN
npx wrangler secret put CRON_SECRET
npx wrangler secret put TELEGRAM_WEBHOOK_SECRET
```

4. Деплой:

```powershell
npm run deploy
```

После деплоя Cloudflare Cron Trigger будет вызывать Worker каждую минуту.
Отдельный cron-jobs.org больше не нужен.

## Telegram webhook

После деплоя откройте защищённый endpoint:

```text
https://<worker-url>/api/set-webhook?secret=<CRON_SECRET>
```

Он установит webhook на:

```text
https://<worker-url>/api/telegram
```

Если задан `TELEGRAM_WEBHOOK_SECRET`, Worker будет принимать webhook-запросы
только с Telegram-заголовком `X-Telegram-Bot-Api-Secret-Token`.

После изменений в коде webhook можно безопасно вызвать повторно. Это обновит
список allowed updates, включая `callback_query` для inline-кнопок.

Бот `@mlb_daily_results_bot` должен быть администратором канала с правом
публиковать и редактировать сообщения.

## Проверки

Health:

```text
https://<worker-url>/api/health
```

Ручная проверка cron:

```text
https://<worker-url>/api/cron?secret=<CRON_SECRET>
```

Ручное создание/обновление меню:

```text
https://<worker-url>/api/menu?secret=<CRON_SECRET>
```

Ручная проверка конкретной даты:

```text
https://<worker-url>/api/cron?secret=<CRON_SECRET>&date=2026-05-03
```

Логи:

```powershell
npm run tail
```
