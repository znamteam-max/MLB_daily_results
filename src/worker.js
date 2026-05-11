const MLB_API = "https://statsapi.mlb.com/api/v1";
const TG_API = "https://api.telegram.org";

const MONTHS_RU = {
  1: "января",
  2: "февраля",
  3: "марта",
  4: "апреля",
  5: "мая",
  6: "июня",
  7: "июля",
  8: "августа",
  9: "сентября",
  10: "октября",
  11: "ноября",
  12: "декабря",
};

const TEAM_RU_BY_ABBR = {
  ARI: "Даймондбэкс",
  ATH: "Атлетикс",
  ATL: "Брэйвз",
  BAL: "Ориолс",
  BOS: "Ред Сокс",
  CHC: "Кабс",
  CIN: "Редс",
  CLE: "Гардианс",
  COL: "Рокиз",
  CWS: "Уайт Сокс",
  DET: "Тайгерс",
  HOU: "Астрос",
  KC: "Роялс",
  LAA: "Энджелс",
  LAD: "Доджерс",
  MIA: "Марлинс",
  MIL: "Брюэрс",
  MIN: "Твинс",
  NYM: "Метс",
  NYY: "Янкис",
  OAK: "Атлетикс",
  PHI: "Филлис",
  PIT: "Пайрэтс",
  SD: "Падрес",
  SEA: "Маринерс",
  SF: "Джайентс",
  STL: "Кардиналс",
  TB: "Рейс",
  TEX: "Рейнджерс",
  TOR: "Блю Джейс",
  WSH: "Нэшионалс",
};

const TEAM_RU_BY_NAME = {
  "Arizona Diamondbacks": "Даймондбэкс",
  Athletics: "Атлетикс",
  "Atlanta Braves": "Брэйвз",
  "Baltimore Orioles": "Ориолс",
  "Boston Red Sox": "Ред Сокс",
  "Chicago Cubs": "Кабс",
  "Chicago White Sox": "Уайт Сокс",
  "Cincinnati Reds": "Редс",
  "Cleveland Guardians": "Гардианс",
  "Colorado Rockies": "Рокиз",
  "Detroit Tigers": "Тайгерс",
  "Houston Astros": "Астрос",
  "Kansas City Royals": "Роялс",
  "Los Angeles Angels": "Энджелс",
  "Los Angeles Dodgers": "Доджерс",
  "Miami Marlins": "Марлинс",
  "Milwaukee Brewers": "Брюэрс",
  "Minnesota Twins": "Твинс",
  "New York Mets": "Метс",
  "New York Yankees": "Янкис",
  "Oakland Athletics": "Атлетикс",
  "Philadelphia Phillies": "Филлис",
  "Pittsburgh Pirates": "Пайрэтс",
  "San Diego Padres": "Падрес",
  "San Francisco Giants": "Джайентс",
  "Seattle Mariners": "Маринерс",
  "St. Louis Cardinals": "Кардиналс",
  "Tampa Bay Rays": "Рейс",
  "Texas Rangers": "Рейнджерс",
  "Toronto Blue Jays": "Блю Джейс",
  "Washington Nationals": "Нэшионалс",
};

const PLAYER_RU_DEFAULTS = {
  "Aaron Bummer": "Аарон Баммер",
  "Aaron Civale": "Аарон Сивале",
  "Aaron Judge": "Аарон Джадж",
  "Adrian Del Castillo": "Адриан дель Кастийо",
  "Andrew Morris": "Эндрю Моррис",
  "Ben Rice": "Бен Райс",
  "Brant Hurter": "Брэнт Хёртер",
  "Brian Abreu": "Брайан Абреу",
  "Bryan Abreu": "Брайан Абреу",
  "Bryson Stott": "Брайсон Стотт",
  "Caleb Kilian": "Калеб Килиан",
  "Chase DeLauter": "Чейз Делотер",
  "Chris Bubic": "Крис Бубич",
  "Chris Paddack": "Крис Пэддак",
  "Clay Holmes": "Клей Холмс",
  "Colby Thomas": "Колби Томас",
  "Daniel Lynch": "Дэниел Линч",
  "Derek Hill": "Дерек Хилл",
  "Drew Romo": "Дрю Ромо",
  "Dustin May": "Дастин Мэй",
  "Esteury Ruiz": "Эстеури Руис",
  "Fernando Cruz": "Фернандо Круз",
  "Gabriel Moreno": "Габриэль Морено",
  "Grant Wolfram": "Грант Вулфрэм",
  "Gregory Soto": "Грегори Сото",
  "Ian Seymour": "Иэн Сеймур",
  "Jack Kochanowicz": "Джек Кохановиц",
  "Jack Leiter": "Джек Лайтер",
  "Jarren Duran": "Джаррен Дюран",
  "Jason Adam": "Джейсон Адам",
  "Jason Dominguez": "Джейсон Домингес",
  "Jasson Dominguez": "Джейсон Домингес",
  "Jasson Domínguez": "Джейсон Домингес",
  "Jesús Luzardo": "Хесус Лусардо",
  "Jesus Luzardo": "Хесус Лусардо",
  "Jonah Heim": "Джона Хайм",
  "Jorge Mateo": "Хорхе Матео",
  "Justin Topa": "Джастин Топа",
  "Justin Wrobleski": "Джастин Вроблески",
  "Kazuma Okamoto": "Кадзума Окамото",
  "Kris Bubic": "Крис Бубич",
  "Kyle Freeland": "Кайл Фриленд",
  "Logan Henderson": "Логан Хендерсон",
  "Luis Castillo": "Луис Кастийо",
  "Manny Machado": "Мэнни Мачадо",
  "Mark Vientos": "Марк Виентос",
  "Mason Miller": "Мейсон Миллер",
  "Matthew Boyd": "Мэттью Бойд",
  "Merrill Kelly": "Меррилл Келли",
  "Mickey Moniak": "Микки Мониак",
  "Miguel Andujar": "Мигель Андухар",
  "Miguel Andújar": "Мигель Андухар",
  "Moises Ballesteros": "Мойсес Байестерос",
  "Moisés Ballesteros": "Мойсес Байестерос",
  "Parker Messick": "Паркер Мессик",
  "Richard Lovelady": "Ричард Лавледи",
  "Spencer Torkelson": "Спенсер Торкелсон",
  "Tanner Scott": "Таннер Скотт",
  "T.J. Rumfield": "Ти Джей Рамфилд",
  "TJ Rumfield": "Ти Джей Рамфилд",
  "Tony Santillan": "Тони Сантийян",
  "Trey Yesavage": "Трей Йесаведж",
  "Tyler Davis": "Тайлер Дэвис",
  "Tyler Soderstrom": "Тайлер Содерстром",
  "Tyler Soderström": "Тайлер Содерстром",
  "Zack Gelof": "Зак Гелоф",
  "Zack Kelly": "Зак Келли",
  "Zach Littell": "Зак Литтелл",
};

const WORD_RU = {
  aaron: "Аарон",
  adam: "Адам",
  adrian: "Адриан",
  andrew: "Эндрю",
  anthony: "Энтони",
  austin: "Остин",
  ben: "Бен",
  brant: "Брэнт",
  brian: "Брайан",
  bryan: "Брайан",
  bryson: "Брайсон",
  caleb: "Калеб",
  chase: "Чейз",
  chris: "Крис",
  clay: "Клей",
  daniel: "Дэниел",
  derek: "Дерек",
  drew: "Дрю",
  dustin: "Дастин",
  fernando: "Фернандо",
  gabriel: "Габриэль",
  grant: "Грант",
  gregory: "Грегори",
  ian: "Иэн",
  jack: "Джек",
  jarren: "Джаррен",
  jason: "Джейсон",
  jasson: "Джейсон",
  jesus: "Хесус",
  jesús: "Хесус",
  jonah: "Джона",
  jorge: "Хорхе",
  justin: "Джастин",
  kris: "Крис",
  kyle: "Кайл",
  logan: "Логан",
  luis: "Луис",
  manny: "Мэнни",
  mark: "Марк",
  mason: "Мейсон",
  matthew: "Мэттью",
  merrill: "Меррилл",
  mickey: "Микки",
  miguel: "Мигель",
  parker: "Паркер",
  richard: "Ричард",
  spencer: "Спенсер",
  tanner: "Таннер",
  tony: "Тони",
  trey: "Трей",
  tyler: "Тайлер",
  zack: "Зак",
  zach: "Зак",
};

const LETTER_NAMES = {
  a: "Эй",
  b: "Би",
  c: "Си",
  d: "Ди",
  e: "И",
  f: "Эф",
  g: "Джи",
  h: "Эйч",
  i: "Ай",
  j: "Джей",
  k: "Кей",
  l: "Эл",
  m: "Эм",
  n: "Эн",
  o: "Оу",
  p: "Пи",
  q: "Кью",
  r: "Ар",
  s: "Эс",
  t: "Ти",
  u: "Ю",
  v: "Ви",
  w: "Дабл-ю",
  x: "Экс",
  y: "Уай",
  z: "Зи",
};

const DEFAULT_PLAYER_MAP = new Map(Object.entries(PLAYER_RU_DEFAULTS).map(([k, v]) => [normKey(k), v]));
const DEFAULT_TEAM_MAP = new Map([
  ...Object.entries(TEAM_RU_BY_ABBR).map(([k, v]) => [normKey(k), v]),
  ...Object.entries(TEAM_RU_BY_NAME).map(([k, v]) => [normKey(k), v]),
]);

export default {
  async fetch(request, env) {
    return route(request, env);
  },

  async scheduled(_controller, env, _ctx) {
    if (!isTrue(env.AUTO_POST, true)) return;
    const results = await cronCheckOnce(env);
    console.log(JSON.stringify({ results }));
  },
};

async function route(request, env) {
  const url = new URL(request.url);
  const path = normalizePath(url.pathname);

  try {
    if (path === "/" || path === "/api") {
      return jsonResponse({
        ok: true,
        service: "mlb-daily-results-cloudflare",
        endpoints: ["/api/health", "/api/telegram", "/api/cron", "/api/set-webhook"],
      });
    }

    if (path === "/health" || path === "/api/health") {
      return jsonResponse({
        ok: true,
        cloudflare: true,
        state: env.MLB_STATE ? "kv" : "missing",
        telegram_token: Boolean(env.TELEGRAM_BOT_TOKEN),
        telegram_webhook_secret: Boolean(env.TELEGRAM_WEBHOOK_SECRET),
        callback_query: true,
        target_chat_id: env.TARGET_CHAT_ID || "-1003643946438",
        auto_post: isTrue(env.AUTO_POST, true),
      });
    }

    if (path === "/telegram" || path === "/api/telegram") {
      if (request.method === "GET") {
        return jsonResponse({ ok: true, service: "telegram-webhook" });
      }
      if (request.method !== "POST") {
        return jsonResponse({ ok: false, error: "method not allowed" }, 405);
      }
      const webhookAuth = requireTelegramWebhookSecret(request, env);
      if (webhookAuth) return webhookAuth;
      const update = await request.json();
      await handleUpdate(env, update);
      return jsonResponse({ ok: true });
    }

    if (path === "/cron" || path === "/api/cron") {
      const auth = requireCronSecret(request, env, url);
      if (auth) return auth;
      const targetDate = parseOptionalDate(url.searchParams.get("date") || "");
      const results = targetDate ? [await checkSingleDate(env, targetDate)] : await cronCheckOnce(env);
      return jsonResponse({ ok: true, results });
    }

    if (path === "/set-webhook" || path === "/api/set-webhook") {
      const auth = requireCronSecret(request, env, url);
      if (auth) return auth;
      const webhookUrl = url.searchParams.get("url") || `${url.origin}/api/telegram`;
      const payload = {
        url: webhookUrl,
        allowed_updates: ["message", "edited_message", "channel_post", "edited_channel_post", "callback_query"],
      };
      if (env.TELEGRAM_WEBHOOK_SECRET) {
        payload.secret_token = env.TELEGRAM_WEBHOOK_SECRET;
      }
      const result = await telegramRequest(env, "setWebhook", payload);
      return jsonResponse({ ok: true, webhook_url: webhookUrl, telegram: result });
    }

    return jsonResponse({ ok: false, error: "not found" }, 404);
  } catch (error) {
    return jsonResponse({ ok: false, error: String(error?.message || error) }, 500);
  }
}

function normalizePath(pathname) {
  const path = pathname.replace(/\/+$/, "");
  return path || "/";
}

function requireTelegramWebhookSecret(request, env) {
  const expected = String(env.TELEGRAM_WEBHOOK_SECRET || "").trim();
  if (!expected) return null;
  const provided = request.headers.get("x-telegram-bot-api-secret-token") || "";
  if (provided !== expected) {
    return jsonResponse({ ok: false, error: "unauthorized webhook" }, 401);
  }
  return null;
}

function requireCronSecret(request, env, url) {
  const expected = String(env.CRON_SECRET || "").trim();
  if (!expected) {
    return jsonResponse({ ok: false, error: "CRON_SECRET is not set" }, 500);
  }
  const auth = request.headers.get("authorization") || "";
  const provided = auth.toLowerCase().startsWith("bearer ")
    ? auth.slice(7).trim()
    : (url.searchParams.get("secret") || "").trim();
  if (provided !== expected) {
    return jsonResponse({ ok: false, error: "unauthorized" }, 401);
  }
  return null;
}

async function handleUpdate(env, update) {
  if (update.callback_query) {
    await handleCallbackQuery(env, update.callback_query);
    return;
  }

  const message =
    update.message || update.edited_message || update.channel_post || update.edited_channel_post || {};
  const chat = message.chat || {};
  const chatId = chat.id;
  const text = String(message.text || "").trim();
  if (!chatId || !text.startsWith("/")) return;
  if (!isAllowedChat(env, Number(chatId), String(chat.type || ""))) return;

  let answer = "";
  try {
    answer = await handleCommand(env, text);
  } catch (error) {
    answer = `Ошибка: ${String(error?.message || error)}`;
  }
  if (answer) {
    if (typeof answer === "string") {
      await sendMessage(env, chatId, answer);
    } else {
      await sendMessage(env, chatId, answer.text, answer.options || {});
    }
  }
}

async function handleCallbackQuery(env, callbackQuery) {
  const data = String(callbackQuery.data || "");
  if (!data.startsWith("edit_names:")) {
    await answerCallbackQuery(env, callbackQuery.id, "Команда не распознана.");
    return;
  }

  const gameDate = data.split(":", 2)[1] || "";
  const text = [
    `Правка фамилий за ${gameDate}`,
    "Отправь в эту группу:",
    "/fix English Name = Русское Имя",
    "Я запомню написание и обновлю последний пост.",
  ].join("\n");

  await answerCallbackQuery(env, callbackQuery.id, "Отправь /fix English Name = Русское Имя. Правка сохранится навсегда.", true);

  const chat = callbackQuery.message?.chat || {};
  const chatId = chat.id;
  const messageId = callbackQuery.message?.message_id;
  if (chatId && chat.type !== "channel") {
    await sendMessage(env, chatId, text, messageId ? { reply_to_message_id: messageId } : {});
  }
}

function isAllowedChat(env, chatId, chatType) {
  const targetChatId = Number(env.TARGET_CHAT_ID || "-1003643946438");
  const configured = parseChatIds(env.ADMIN_CHAT_IDS || "");
  const admins = configured.size ? configured : new Set([targetChatId]);
  return admins.has(chatId) || chatType === "private";
}

async function handleCommand(env, raw) {
  const [first, ...restParts] = raw.split(/\s+/);
  const cmd = first.split("@", 1)[0].toLowerCase();
  const rest = raw.slice(first.length).trim();
  const currentDate = currentGameDate(env.MLB_TZ || "America/New_York");

  if (cmd === "/start" || cmd === "/help") return HELP_TEXT;
  if (cmd === "/today") {
    const d = parseOptionalDate(rest) || currentDate;
    return {
      text: await buildResults(env, d, true),
      options: { parse_mode: "HTML", reply_markup: editNamesMarkup(d) },
    };
  }
  if (cmd === "/schedule") {
    const d = parseOptionalDate(rest) || currentDate;
    return buildSchedule(env, d);
  }
  if (cmd === "/status") {
    const d = parseOptionalDate(rest) || currentDate;
    const posted = Boolean(await getPost(env, d));
    return statusSummary(env, d, posted);
  }
  if (cmd === "/post") {
    const d = parseOptionalDate(rest) || currentDate;
    const text = await buildResults(env, d, false);
    return sendOrEditChannelPost(env, d, text);
  }
  if (cmd === "/refresh") {
    const d = parseOptionalDate(rest) || currentDate;
    return refreshPost(env, d);
  }
  if (cmd === "/fix" || cmd === "/player" || cmd === "/name") {
    const [source, target] = splitAssignment(rest);
    await putTranslation(env, "player", source, target);
    let message = `Запомнил: ${source} → ${target}`;
    const latest = await latestPost(env);
    if (latest) message += `\n${await refreshPost(env, latest.game_date)}`;
    return message;
  }
  if (cmd === "/team") {
    const [source, target] = splitAssignment(rest);
    await putTranslation(env, "team", source, target);
    let message = `Запомнил команду: ${source} → ${target}`;
    const latest = await latestPost(env);
    if (latest) message += `\n${await refreshPost(env, latest.game_date)}`;
    return message;
  }
  if (cmd === "/replace") {
    const [source, target] = splitAssignment(rest);
    const latest = await latestPost(env);
    if (!latest) return "Нет сохранённых постов для правки.";
    if (!latest.text.includes(source)) return `Не нашёл в последнем посте: ${source}`;
    const text = latest.text.split(source).join(target);
    await editMessage(env, latest.chat_id, latest.message_id, text, postMessageOptions(latest.game_date));
    await updatePostText(env, latest.game_date, text);
    return `Заменил в посте за ${latest.game_date}: ${source} → ${target}`;
  }
  if (cmd === "/dict") {
    const rows = await listTranslations(env, rest);
    if (!rows.length) return "Словарь правок пока пуст.";
    return rows.map((row) => `${row.kind}: ${row.source} → ${row.target}`).join("\n");
  }
  if (cmd === "/unknown") {
    const d = parseOptionalDate(rest) || currentDate;
    const unknown = await unknownPlayers(env, d);
    if (!unknown.length) return "Новых имён без ручной правки не нашёл.";
    return [`Имена без ручной правки за ${d}:`, ...unknown.slice(0, 40).map(([src, guess]) => `${src} → ${guess}`)].join("\n");
  }
  return HELP_TEXT;
}

const HELP_TEXT = `Команды MLB-бота:
/today [YYYY-MM-DD] - показать пост результатов
/schedule [YYYY-MM-DD] - расписание и количество матчей
/status [YYYY-MM-DD] - статус игрового дня
/post [YYYY-MM-DD] - отправить/обновить пост в канале
/refresh [YYYY-MM-DD] - перегенерировать уже опубликованный пост
/fix English Name = Русское Имя - запомнить имя игрока
/team Twins = Твинс - запомнить название команды
/replace старый текст = новый текст - поправить последний пост
/dict [поиск] - показать словарь правок
/unknown [YYYY-MM-DD] - показать имена без ручной правки`;

async function cronCheckOnce(env) {
  if (!isTrue(env.AUTO_POST, true)) return ["AUTO_POST=false"];
  const today = dateInTZ(env.MLB_TZ || "America/New_York");
  const lookback = numberOrDefault(env.AUTO_LOOKBACK_DAYS, 2);
  const results = [];

  for (let delta = 0; delta < lookback; delta += 1) {
    const d = addDays(today, -delta);
    if (await getPost(env, d)) {
      results.push(`${d}: already posted`);
      continue;
    }
    results.push(await checkSingleDate(env, d));
  }
  return results;
}

async function checkSingleDate(env, d) {
  if (await getPost(env, d)) return `${d}: already posted`;
  const games = await gamesForDate(d);
  if (!allDone(games)) {
    const final = games.filter(isFinalGame).length;
    return `${d}: not ready (${final}/${games.length} final)`;
  }
  const text = await buildResults(env, d, false, games);
  return sendOrEditChannelPost(env, d, text);
}

async function sendOrEditChannelPost(env, d, text) {
  if (text.length > 4096) throw new Error(`Telegram message is too long: ${text.length} chars`);
  const options = postMessageOptions(d);
  const existing = await getPost(env, d);
  if (existing) {
    await editMessage(env, existing.chat_id, existing.message_id, text, options);
    await savePost(env, d, existing.chat_id, existing.message_id, text);
    return `Обновил пост за ${d}.`;
  }
  const chatId = env.TARGET_CHAT_ID || "-1003643946438";
  const messageId = await sendMessage(env, chatId, text, options);
  await savePost(env, d, chatId, messageId, text);
  return `Опубликовал пост за ${d}.`;
}

async function refreshPost(env, d) {
  const existing = await getPost(env, d);
  if (!existing) return `За ${d} ещё нет сохранённого поста. Используй /post ${d}.`;
  const text = await buildResults(env, d, false);
  await editMessage(env, existing.chat_id, existing.message_id, text, postMessageOptions(d));
  await savePost(env, d, existing.chat_id, existing.message_id, text);
  return `Перегенерировал и обновил пост за ${d}.`;
}

async function buildResults(env, d, includePending = true, knownGames = null) {
  const games = knownGames || (await gamesForDate(d));
  const header = `⚾️ МЛБ • ${seriesTitle(games)} • ${ruDate(d)}`;
  if (!games.length) return `${header}\n\nМатчей нет.`;

  const translator = createTranslator(env);
  const pitcherRecords = await preloadPitcherSeasonRecords(games);
  const qualityStartWinners = await preloadQualityStartWinners(games);
  const blocks = [header];

  for (const game of games.slice().sort(gameSortKey)) {
    if (isFinalGame(game)) {
      blocks.push(await finalGameBlock(env, translator, game, d, pitcherRecords, qualityStartWinners));
    } else if (includePending) {
      blocks.push(await pendingGameBlock(env, translator, game));
    }
  }
  return blocks.filter(Boolean).join("\n\n").trim();
}

async function buildSchedule(env, d) {
  const games = await gamesForDate(d);
  const translator = createTranslator(env);
  const count = games.length;
  const lines = [`⚾️ МЛБ • Расписание • ${ruDate(d)}`, `${count} ${pluralRu(count, "матч", "матча", "матчей")}`];
  if (!games.length) return lines.join("\n");
  lines.push("");
  for (const game of games.slice().sort(gameSortKey)) {
    const home = await teamLineName(env, translator, game, "home");
    const away = await teamLineName(env, translator, game, "away");
    const status = statusRu(game) || gameLocalTime(env, game);
    lines.push(`${home} — ${away} • ${status}`);
  }
  return lines.join("\n").trim();
}

async function statusSummary(env, d, posted) {
  const games = await gamesForDate(d);
  const total = games.length;
  const final = games.filter(isFinalGame).length;
  const active = games.filter(isActiveGame).length;
  const pending = Math.max(0, total - final - active);
  const ready = total > 0 && final === total;
  return [
    `MLB ${d}`,
    `Всего: ${total}`,
    `Завершено: ${final}`,
    `В игре: ${active}`,
    `Ожидают: ${pending}`,
    `Готово к публикации: ${ready ? "да" : "нет"}`,
    `Опубликовано: ${posted ? "да" : "нет"}`,
  ].join("\n");
}

async function unknownPlayers(env, d) {
  const games = await gamesForDate(d);
  const translator = createTranslator(env);
  const names = new Set();
  for (const game of games) {
    const decisions = game.decisions || {};
    for (const key of ["winner", "loser", "save"]) {
      if (decisions[key]?.fullName) names.add(decisions[key].fullName);
    }
    for (const hr of game.homeRuns || []) {
      const batter = hr.matchup?.batter?.fullName;
      if (batter) names.add(batter);
    }
  }
  const out = [];
  for (const name of [...names].sort((a, b) => normKey(a).localeCompare(normKey(b)))) {
    if (await getTranslation(env, "player", name)) continue;
    if (DEFAULT_PLAYER_MAP.has(normKey(name)) || DEFAULT_PLAYER_MAP.has(normKey(cleanPlayerSource(name)))) continue;
    out.push([name, await translator.player(name)]);
  }
  return out;
}

async function finalGameBlock(env, translator, game, d, pitcherRecords, qualityStartWinners) {
  const home = await teamScoreLine(env, translator, game, "home");
  const away = await teamScoreLine(env, translator, game, "away");
  const decisions = await decisionsLine(translator, game, pitcherRecords, qualityStartWinners);
  const homers = await homeRunsLine(translator, game);
  const lines = [home, away, "", decisions];
  if (homers) lines.push(homers);
  return lines.join("\n").trim();
}

async function pendingGameBlock(env, translator, game) {
  const home = await teamLineName(env, translator, game, "home");
  const away = await teamLineName(env, translator, game, "away");
  return `${home}: —\n${away}: —\n${statusRu(game) || gameLocalTime(env, game)}`;
}

async function teamScoreLine(env, translator, game, side) {
  const teamData = game.teams?.[side] || {};
  const team = teamData.team || {};
  const name = await translator.team(team);
  const score = intOrZero(teamData.score);
  const record = teamData.leagueRecord || {};
  return `${env.TEAM_EMOJI || "😀"} <b>${escapeHtml(name)}</b>: ${score} (${intOrZero(record.wins)}-${intOrZero(record.losses)})`;
}

async function teamLineName(env, translator, game, side) {
  const team = game.teams?.[side]?.team || {};
  return `${env.TEAM_EMOJI || "😀"} ${await translator.team(team)}`;
}

async function decisionsLine(translator, game, pitcherRecords, qualityStartWinners) {
  const decisions = game.decisions || {};
  const parts = [];
  if (decisions.winner) parts.push(`Победа: ${await pitcherWithRecord(translator, decisions.winner, pitcherRecords, "wl", qualityStartWinners.has(Number(decisions.winner.id)))}`);
  if (decisions.loser) parts.push(`поражение: ${await pitcherWithRecord(translator, decisions.loser, pitcherRecords, "wl")}`);
  if (decisions.save) parts.push(`сейв: ${await pitcherWithRecord(translator, decisions.save, pitcherRecords, "save")}`);
  return parts.length ? parts.join("; ") : "Победа/поражение: —";
}

async function pitcherWithRecord(translator, person, pitcherRecords, mode, qualityStart = false) {
  const name = await translator.player(person.fullName || "");
  const record = pitcherRecords.get(Number(person.id));
  const label = `${escapeHtml(name)}${qualityStart ? " 🎯" : ""}`;
  if (!record) return label;
  if (mode === "save") return `${label} (${record.saves})`;
  return `${label} (${record.wins}-${record.losses})`;
}

async function homeRunsLine(translator, game) {
  const bySide = { home: new Map(), away: new Map() };
  for (const hr of game.homeRuns || []) {
    const half = String(hr.about?.halfInning || "").toLowerCase();
    const side = half === "top" ? "away" : "home";
    const rawName = String(hr.matchup?.batter?.fullName || "").trim();
    if (!rawName) continue;
    const key = normKey(rawName);
    if (!bySide[side].has(key)) {
      bySide[side].set(key, {
        name: await translator.player(rawName),
        count: 0,
        seasonTotal: null,
      });
    }
    const item = bySide[side].get(key);
    item.count += 1;
    const total = hrTotal(hr);
    if (total !== null) item.seasonTotal = total;
  }

  const home = formatHrItems([...bySide.home.values()]);
  const away = formatHrItems([...bySide.away.values()]);
  if (!home && !away) return "";
  const value = home && away ? `${home} — ${away}` : home || away;
  return `Хоум-раны: ${value}`;
}

function formatHrItems(items) {
  return items
    .map((item) => {
      const fire = item.count >= 2 ? " 🔥" : "";
      const name = escapeHtml(item.name);
      if (item.count > 1 && item.seasonTotal !== null) return `${name} ${item.count} (${item.seasonTotal})${fire}`;
      if (item.seasonTotal !== null) return `${name} (${item.seasonTotal})${fire}`;
      if (item.count > 1) return `${name} ${item.count}${fire}`;
      return `${name}${fire}`;
    })
    .join(", ");
}

function hrTotal(hr) {
  const desc = String(hr.result?.description || "");
  const match = desc.match(/homers\s+\((\d+)\)/i);
  return match ? Number(match[1]) : null;
}

async function gamesForDate(d) {
  const url = `${MLB_API}/schedule?sportId=1&date=${d}&hydrate=team,linescore,decisions,homeRuns`;
  const data = await fetchJson(url);
  return data.dates?.[0]?.games || [];
}

async function preloadPitcherSeasonRecords(games) {
  const ids = new Set();
  let season = new Date().getUTCFullYear();
  for (const game of games) {
    season = intOrZero(game.season) || season;
    const decisions = game.decisions || {};
    for (const key of ["winner", "loser", "save"]) {
      const id = intOrZero(decisions[key]?.id);
      if (id) ids.add(id);
    }
  }
  const records = new Map();
  const allIds = [...ids];
  for (let i = 0; i < allIds.length; i += 40) {
    const chunk = allIds.slice(i, i + 40);
    const hydrate = encodeURIComponent(`stats(group=[pitching],type=[season],season=${season})`);
    const data = await fetchJson(`${MLB_API}/people?personIds=${chunk.join(",")}&hydrate=${hydrate}`);
    for (const person of data.people || []) {
      const split = person.stats?.find((group) => group.splits?.length)?.splits?.[0];
      const stat = split?.stat || {};
      records.set(Number(person.id), {
        wins: intOrZero(stat.wins),
        losses: intOrZero(stat.losses),
        saves: intOrZero(stat.saves),
      });
    }
  }
  return records;
}

async function preloadQualityStartWinners(games) {
  const winners = new Set();
  const finalGames = games.filter((game) => isFinalGame(game) && game.decisions?.winner?.id && game.gamePk);
  await Promise.all(
    finalGames.map(async (game) => {
      try {
        const winnerId = Number(game.decisions.winner.id);
        const boxscore = await fetchJson(`${MLB_API}/game/${game.gamePk}/boxscore`);
        const pitcher = findBoxscorePlayer(boxscore, winnerId);
        const pitching = pitcher?.stats?.pitching || {};
        const started = intOrZero(pitching.gamesStarted) > 0;
        const outs = intOrZero(pitching.outs) || inningsToOuts(pitching.inningsPitched);
        const earnedRuns = intOrZero(pitching.earnedRuns);
        if (started && outs >= 18 && earnedRuns <= 3) {
          winners.add(winnerId);
        }
      } catch (error) {
        console.log(`quality-start lookup failed for ${game.gamePk}: ${String(error?.message || error)}`);
      }
    }),
  );
  return winners;
}

function findBoxscorePlayer(boxscore, playerId) {
  for (const side of ["home", "away"]) {
    const players = boxscore?.teams?.[side]?.players || {};
    const direct = players[`ID${playerId}`];
    if (direct) return direct;
    for (const player of Object.values(players)) {
      if (Number(player?.person?.id) === Number(playerId)) return player;
    }
  }
  return null;
}

function inningsToOuts(value) {
  const raw = String(value || "");
  if (!raw) return 0;
  const [whole, fraction = "0"] = raw.split(".");
  const fullInnings = intOrZero(whole);
  const partial = fraction === "1" ? 1 : fraction === "2" ? 2 : 0;
  return fullInnings * 3 + partial;
}

function createTranslator(env) {
  const cache = new Map();
  async function translated(kind, source) {
    const key = `${kind}:${normKey(source)}`;
    if (cache.has(key)) return cache.get(key);
    const value = await getTranslation(env, kind, source);
    cache.set(key, value);
    return value;
  }
  return {
    async team(team) {
      const candidates = [team.abbreviation, team.teamName, team.clubName, team.name, team.shortName].filter(Boolean).map(String);
      for (const candidate of candidates) {
        const override = await translated("team", candidate);
        if (override) return override;
        const fallback = DEFAULT_TEAM_MAP.get(normKey(candidate));
        if (fallback) return fallback;
      }
      return wordsRu(team.teamName || team.name || "Team");
    },
    async player(name) {
      const raw = String(name || "").replace(/\s+/g, " ").trim();
      if (!raw) return "";
      const override = await translated("player", raw);
      if (override) return override;
      const clean = cleanPlayerSource(raw);
      if (clean !== raw) {
        const cleanOverride = await translated("player", clean);
        if (cleanOverride) return cleanOverride;
      }
      return DEFAULT_PLAYER_MAP.get(normKey(raw)) || DEFAULT_PLAYER_MAP.get(normKey(clean)) || wordsRu(clean);
    },
  };
}

async function getTranslation(env, kind, source) {
  const kinds = kind === "any" ? [kind] : [kind, "any"];
  for (const k of kinds) {
    const row = await kvGetJson(env, translationKey(k, source));
    if (row?.target) return row.target;
  }
  return null;
}

async function putTranslation(env, kind, source, target) {
  const payload = {
    kind,
    source: source.trim(),
    source_norm: normKey(source),
    target: target.trim(),
    updated_at: new Date().toISOString(),
  };
  await env.MLB_STATE.put(translationKey(kind, source), JSON.stringify(payload));
}

async function listTranslations(env, query = "", limit = 30) {
  const list = await env.MLB_STATE.list({ prefix: "translation:", limit: 1000 });
  const qNorm = normKey(query);
  const qLower = query.toLowerCase();
  const rows = [];
  for (const item of list.keys) {
    const row = await kvGetJson(env, item.name);
    if (!row) continue;
    if (query && !row.source_norm.includes(qNorm) && !String(row.target || "").toLowerCase().includes(qLower)) continue;
    rows.push(row);
  }
  rows.sort((a, b) => String(b.updated_at || "").localeCompare(String(a.updated_at || "")));
  return rows.slice(0, limit);
}

function translationKey(kind, source) {
  return `translation:${kind}:${normKey(source)}`;
}

async function savePost(env, d, chatId, messageId, text) {
  const existing = await getPost(env, d);
  const now = new Date().toISOString();
  const payload = {
    game_date: d,
    chat_id: String(chatId),
    message_id: Number(messageId),
    text,
    posted_at: existing?.posted_at || now,
    updated_at: now,
  };
  await env.MLB_STATE.put(`post:${d}`, JSON.stringify(payload));
  await env.MLB_STATE.put("latest_post_date", d);
}

async function getPost(env, d) {
  return kvGetJson(env, `post:${d}`);
}

async function latestPost(env) {
  const latestDate = await env.MLB_STATE.get("latest_post_date");
  if (latestDate) {
    const post = await getPost(env, latestDate);
    if (post) return post;
  }
  const list = await env.MLB_STATE.list({ prefix: "post:", limit: 1000 });
  const dates = list.keys.map((item) => item.name.replace(/^post:/, "")).sort();
  return dates.length ? getPost(env, dates[dates.length - 1]) : null;
}

async function updatePostText(env, d, text) {
  const post = await getPost(env, d);
  if (!post) return;
  post.text = text;
  post.updated_at = new Date().toISOString();
  await env.MLB_STATE.put(`post:${d}`, JSON.stringify(post));
}

async function kvGetJson(env, key) {
  const raw = await env.MLB_STATE.get(key);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

async function telegramRequest(env, method, payload) {
  if (!env.TELEGRAM_BOT_TOKEN) throw new Error("TELEGRAM_BOT_TOKEN is not set");
  const response = await fetch(`${TG_API}/bot${env.TELEGRAM_BOT_TOKEN}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok || !data.ok) {
    throw new Error(`Telegram API error: ${JSON.stringify(data)}`);
  }
  return data;
}

async function answerCallbackQuery(env, callbackQueryId, text, showAlert = false) {
  await telegramRequest(env, "answerCallbackQuery", {
    callback_query_id: callbackQueryId,
    text,
    show_alert: showAlert,
  });
}

function postMessageOptions(gameDate) {
  return {
    parse_mode: "HTML",
    reply_markup: editNamesMarkup(gameDate),
  };
}

function editNamesMarkup(gameDate) {
  return {
    inline_keyboard: [
      [{ text: "✏️ Править фамилии", callback_data: `edit_names:${gameDate}` }],
    ],
  };
}

async function sendMessage(env, chatId, text, extra = {}) {
  const data = await telegramRequest(env, "sendMessage", {
    chat_id: chatId,
    text,
    disable_web_page_preview: true,
    ...extra,
  });
  return Number(data.result?.message_id || 0);
}

async function editMessage(env, chatId, messageId, text, extra = {}) {
  await telegramRequest(env, "editMessageText", {
    chat_id: chatId,
    message_id: Number(messageId),
    text,
    disable_web_page_preview: true,
    ...extra,
  });
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      accept: "application/json",
      "user-agent": "MLB Daily Results Cloudflare Worker/1.0",
    },
  });
  if (!response.ok) throw new Error(`GET failed ${response.status}: ${url}`);
  return response.json();
}

function seriesTitle(games) {
  const types = new Set(games.map((game) => String(game.gameType || "")));
  if (!types.size || (types.size === 1 && types.has("R"))) return "Регулярный чемпионат";
  if (types.has("P")) return "Плей-офф";
  if (types.has("S")) return "Предсезонка";
  return "Матчи";
}

function gameSortKey(a, b) {
  const da = String(a.gameDate || "");
  const db = String(b.gameDate || "");
  if (da !== db) return da.localeCompare(db);
  const ha = String(a.teams?.home?.team?.name || "");
  const hb = String(b.teams?.home?.team?.name || "");
  if (ha !== hb) return ha.localeCompare(hb);
  return intOrZero(a.gamePk) - intOrZero(b.gamePk);
}

function isFinalGame(game) {
  const status = game.status || {};
  return (
    String(status.abstractGameState || "").toLowerCase() === "final" ||
    ["F", "O"].includes(String(status.statusCode || "").toUpperCase()) ||
    ["F", "O"].includes(String(status.codedGameState || "").toUpperCase())
  );
}

function isActiveGame(game) {
  return String(game.status?.abstractGameState || "").toLowerCase() === "live";
}

function isClosedNonFinal(game) {
  const detailed = String(game.status?.detailedState || "").toLowerCase();
  return ["postponed", "cancelled", "suspended"].some((word) => detailed.includes(word));
}

function allDone(games) {
  return games.length > 0 && games.every((game) => isFinalGame(game) || isClosedNonFinal(game));
}

function statusRu(game) {
  const status = game.status || {};
  const abstract = String(status.abstractGameState || "").toLowerCase();
  const detailed = String(status.detailedState || "").toLowerCase();
  if (abstract === "final") return "завершён";
  if (abstract === "live") return "идёт";
  if (detailed.includes("postponed")) return "перенесён";
  if (detailed.includes("cancelled")) return "отменён";
  if (detailed.includes("suspended")) return "приостановлен";
  if (detailed.includes("delayed")) return "задержка";
  return "";
}

function gameLocalTime(env, game) {
  const raw = String(game.gameDate || "");
  if (!raw) return "";
  const dt = new Date(raw);
  const time = new Intl.DateTimeFormat("ru-RU", {
    timeZone: env.LOCAL_TZ || "Europe/Moscow",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).format(dt);
  return `${time} МСК`;
}

function currentGameDate(tz) {
  const parts = datePartsInTZ(new Date(), tz);
  const ymd = `${parts.year}-${pad2(parts.month)}-${pad2(parts.day)}`;
  return Number(parts.hour) < 12 ? addDays(ymd, -1) : ymd;
}

function dateInTZ(tz) {
  const parts = datePartsInTZ(new Date(), tz);
  return `${parts.year}-${pad2(parts.month)}-${pad2(parts.day)}`;
}

function datePartsInTZ(dt, tz) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: tz,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    hourCycle: "h23",
  }).formatToParts(dt);
  const map = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return {
    year: Number(map.year),
    month: Number(map.month),
    day: Number(map.day),
    hour: Number(map.hour),
  };
}

function addDays(ymd, days) {
  const [year, month, day] = ymd.split("-").map(Number);
  const dt = new Date(Date.UTC(year, month - 1, day + days));
  return `${dt.getUTCFullYear()}-${pad2(dt.getUTCMonth() + 1)}-${pad2(dt.getUTCDate())}`;
}

function ruDate(ymd) {
  const [, month, day] = ymd.split("-").map(Number);
  return `${day} ${MONTHS_RU[month]}`;
}

function parseOptionalDate(value) {
  const match = String(value || "").match(/\d{4}-\d{2}-\d{2}/);
  return match ? match[0] : null;
}

function splitAssignment(value) {
  const separators = ["=", "->", "→"];
  for (const sep of separators) {
    if (value.includes(sep)) {
      const [left, ...rightParts] = value.split(sep);
      const right = rightParts.join(sep);
      if (left.trim() && right.trim()) return [left.trim(), right.trim()];
    }
  }
  throw new Error("Нужен формат: /fix English Name = Русское Имя");
}

function parseChatIds(raw) {
  const out = new Set();
  for (const part of String(raw || "").split(/[,\s]+/)) {
    if (!part) continue;
    const n = Number(part);
    if (Number.isFinite(n)) out.add(n);
  }
  return out;
}

function normKey(value) {
  return removeAccents(String(value || ""))
    .toLocaleLowerCase("ru-RU")
    .replace(/[^a-zа-яё0-9]+/gi, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function removeAccents(value) {
  return String(value || "")
    .normalize("NFKD")
    .replace(/\p{M}/gu, "");
}

function cleanPlayerSource(name) {
  return String(name || "")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/\s+(Jr\.?|Sr\.?|II|III|IV|V)$/i, "")
    .trim();
}

function wordsRu(value) {
  return removeAccents(value)
    .split(/(\s+|-|')/)
    .map((token) => {
      if (!token || /^\s+$/.test(token) || token === "-" || token === "'") return token;
      if (token.includes(".") && token.replace(/\./g, "").length <= 3) {
        return token
          .replace(/\./g, "")
          .toLowerCase()
          .split("")
          .map((ch) => LETTER_NAMES[ch] || ch)
          .join(" ");
      }
      return WORD_RU[token.toLowerCase()] || transliterateWord(token);
    })
    .join("")
    .replace(/\s+/g, " ")
    .trim();
}

function transliterateWord(word) {
  const src = removeAccents(word).toLowerCase();
  const replacements = [
    ["sch", "ш"],
    ["tch", "ч"],
    ["ch", "ч"],
    ["sh", "ш"],
    ["ph", "ф"],
    ["th", "т"],
    ["ck", "к"],
    ["qu", "кв"],
    ["ee", "и"],
    ["oo", "у"],
    ["ai", "эй"],
    ["ay", "эй"],
    ["ei", "ей"],
    ["ey", "ей"],
    ["ea", "и"],
    ["ou", "ау"],
    ["ow", "оу"],
    ["au", "о"],
    ["ie", "и"],
    ["ia", "иа"],
    ["io", "ио"],
    ["ll", "лл"],
  ];
  const letters = {
    a: "а",
    b: "б",
    c: "к",
    d: "д",
    e: "е",
    f: "ф",
    g: "г",
    h: "х",
    i: "и",
    j: "дж",
    k: "к",
    l: "л",
    m: "м",
    n: "н",
    o: "о",
    p: "п",
    q: "к",
    r: "р",
    s: "с",
    t: "т",
    u: "у",
    v: "в",
    w: "в",
    x: "кс",
    y: "и",
    z: "з",
  };
  let out = "";
  for (let i = 0; i < src.length; ) {
    let matched = false;
    for (const [latin, cyr] of replacements) {
      if (src.startsWith(latin, i)) {
        out += cyr;
        i += latin.length;
        matched = true;
        break;
      }
    }
    if (matched) continue;
    out += letters[src[i]] || src[i];
    i += 1;
  }
  return out ? out[0].toUpperCase() + out.slice(1) : word;
}

function pluralRu(n, one, few, many) {
  const value = Math.abs(Number(n));
  if (value % 10 === 1 && value % 100 !== 11) return one;
  if (value % 10 >= 2 && value % 10 <= 4 && !(value % 100 >= 12 && value % 100 <= 14)) return few;
  return many;
}

function intOrZero(value) {
  const n = Number(value);
  return Number.isFinite(n) ? Math.trunc(n) : 0;
}

function numberOrDefault(value, fallback) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function isTrue(value, fallback = false) {
  if (value === undefined || value === null || value === "") return fallback;
  return ["1", "true", "yes", "y", "on"].includes(String(value).trim().toLowerCase());
}

function pad2(value) {
  return String(value).padStart(2, "0");
}

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function jsonResponse(payload, status = 200) {
  return new Response(JSON.stringify(payload, null, 2), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}
