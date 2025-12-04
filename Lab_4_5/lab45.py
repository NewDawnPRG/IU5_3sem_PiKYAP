import asyncio
import random
from datetime import datetime, timedelta, timezone, tzinfo
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = ""

GOIDA_PHOTO_URL = "https://m.gjcdn.net/game-header/950/929009-zrkzhsjt-v4.jpg" 

class FixedTimezone(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=3)
    def dst(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return "UTC+3"

MOSCOW_TZ = FixedTimezone()

EXAMS = [
    ("ИУ6", datetime(2025, 12, 20, 9, 0, tzinfo=MOSCOW_TZ)),
    ("ИУ6", datetime(2025, 12, 24, 9, 0, tzinfo=MOSCOW_TZ)),
    ("ИУ5", datetime(2025, 12, 24, 14, 0, tzinfo=MOSCOW_TZ)),
    ("ИУ5", datetime(2025, 7, 3, 14, 0, tzinfo=MOSCOW_TZ))
]

banned_users = {}

GERMAN_JOKES = [
    "Warum nehmen Geister nie den Bus? Weil sie einen Fahrplan haben, der nie eingeholt wird!",
    "Was ist der Unterschied zwischen einer Kamera und einer Kartoffel? Keiner, beide haben Augen!",
    "Warum konnte der Computer nicht schlafen? Weil er einen Virus hatte, der ihn wach hielt!",
    "Wie nennt man einen Frosch, der eine Disco aufmacht? MC Hammer!",
    "Was macht ein Clown im Büro? Faxen!",
    "Warum sind Mathematiker schlechte Gärtner? Weil sie immer Wurzeln ziehen!",
    "Was ist grün und steht im Wald? Ein ungepflücktes Känguru!",
    "Warum tragen Astronauten immer Helm? Weil sie sich vor den Sternschnuppen schützen müssen!",
    "Was ist das Lieblingsessen eines Gespenstes? Spukhetti!",
    "Warum ging der Kühlschrank zum Psychiater? Weil er komplexe hatte!"
]

JAPANESE_JOKES = [
    "なぜ、本は怖がらないの？ページがあるから！",
    "トマトは赤い、でも、走るのは遅い。なぜ？ケチャップだから！",
    "サッカーの試合中に卵が割れた。誰がやった？卵！",
    "なぜ、自転車が立っていられないの？二本足だから！",
    "海の中で一番強いのは？海老！",
    "猫は何と言う？ニャー！",
    "なぜ、鳥は学校に行かないの？空を飛べるから！",
    "電車の中で一番冷たいところは？冷房車！",
    "犬は何と言う？ワン！",
    "なぜ、魚はお金持ち？海に銀行があるから！"
]

RAMMSTEIN_SONGS = [
    "Du Hast - https://www.youtube.com/watch?v=W3q8Od5qJio",
    "Sonne - https://www.youtube.com/watch?v=StZcUAPRRac",
    "Ich Will - https://www.youtube.com/watch?v=qHm9MG9xw1o",
    "Mein Herz brennt - https://www.youtube.com/watch?v=IxuEtL7gxoM",
    "Deutschland - https://www.youtube.com/watch?v=NeQM1c-XCDc"
]

async def timeleft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.now(MOSCOW_TZ)
    response = []

    groups = set(group for group, _ in EXAMS)

    for group in sorted(groups):
        group_exams = [exam_date for g, exam_date in EXAMS if g == group]
        group_response = [f"<b>{group}:</b>"]

        for exam_date in group_exams:
            total_seconds = (exam_date - now).total_seconds()

            if total_seconds <= 0:
                exam_info = "✅ Экзамен уже прошел"
            else:
                days = int(total_seconds // 86400)
                remaining_seconds = total_seconds % 86400
                hours = int(remaining_seconds // 3600)
                minutes = int((remaining_seconds % 3600) // 60)
                exam_info = f"⏳ Осталось: {days} дн. {hours} час. {minutes} мин."

            group_response.append(f"{exam_date.strftime('%d.%m.%Y %H:%M')} - {exam_info}")

        response.append("\n".join(group_response))

    await update.message.reply_text("\n\n".join(response), parse_mode="HTML")

async def random_grade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    grades = [1, 2, 3, 4, 5]
    weights = [1, 20, 30, 20, 9]
    grade = random.choices(grades, weights=weights, k=1)[0]
    await update.message.reply_text(f"Твоя оценка на экзамене - {grade}")

async def kreuz_joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    joke = random.choice(GERMAN_JOKES)
    await update.message.reply_text(f"🇩🇪 Немецкая шутка:\n\n{joke}")

async def boku_joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    joke = random.choice(JAPANESE_JOKES)
    await update.message.reply_text(f"🇯🇵 Японская шутка:\n\n{joke}")

async def rammstein_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    song = random.choice(RAMMSTEIN_SONGS)
    await update.message.reply_text(f"🎵 Слушай Rammstein:\n\n{song}")

async def razrab(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        photos = await context.bot.get_user_profile_photos(context.bot.id, limit=1)
        if photos.total_count > 0:
            photo = photos.photos[0][0]
            await update.message.reply_photo(photo.file_id, caption="👨‍💻 Разработчик в здании!")
        else:
            await update.message.reply_text("⚠️ У бота нет фото профиля!")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def goida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for _ in range(5):
        try:
            await update.message.reply_photo(
                GOIDA_PHOTO_URL,
                caption="ГОЙДА! 🗡️",
                disable_notification=True
            )
            await asyncio.sleep(1)
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка отправки фото: {str(e)}")
            break

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    if not update.message.reply_to_message and not context.args:
        await update.message.reply_text("ℹ️ Ответьте на сообщение пользователя или укажите @username")
        return

    target_user = None

    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user

    elif context.args and context.args[0].startswith('@'):
        username = context.args[0][1:]
        try:
            user = await context.bot.get_chat_member(chat_id, username)
            target_user = user.user
        except Exception:
            pass

    if not target_user:
        await update.message.reply_text("❌ Пользователь не найден")
        return

    if chat_id not in banned_users:
        banned_users[chat_id] = set()

    banned_users[chat_id].add(target_user.id)
    await update.message.reply_text(
        f"🔨 Пользователь @{target_user.username} добавлен в шуточный бан!\n"
        "Теперь на каждое его сообщение я буду отвечать 'Брысь отсюда, нехороший человек'"
    )

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    if chat_id not in banned_users or not banned_users[chat_id]:
        await update.message.reply_text("ℹ️ В этом чате нет забаненных пользователей")
        return

    target_user = None

    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user

    elif context.args and context.args[0].startswith('@'):
        username = context.args[0][1:]
        try:
            user = await context.bot.get_chat_member(chat_id, username)
            target_user = user.user
        except Exception:
            pass

    if target_user:
        if target_user.id in banned_users[chat_id]:
            banned_users[chat_id].remove(target_user.id)
            await update.message.reply_text(
                f"✅ Пользователь @{target_user.username} разбанен!"
            )
        else:
            await update.message.reply_text(
                f"ℹ️ Пользователь @{target_user.username} не был забанен"
            )
    else:
        count = len(banned_users[chat_id])
        banned_users[chat_id].clear()
        await update.message.reply_text(
            f"✅ Все пользователи ({count}) разбанены!"
        )

async def handle_banned_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    if chat_id in banned_users and user_id in banned_users[chat_id]:
        await update.message.reply_text(
            "Брысь отсюда, нехороший человек",
            reply_to_message_id=update.message.message_id
        )

async def send_cactus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with open("video5377644305538117649.mp4", "rb") as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="Вот тебе кактусы! 🌵🌵🌵"
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Не удалось отправить видео: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands = [
        "<b>Доступные команды:</b>",
        "",
        "/timeleft - Время до экзаменов",
        "/random - Случайная оценка",
        "/Kreuzschlitzschraubendreher - Немецкая шутка",
        "/BokuNoHero - Японская шутка",
        "/rammstein - Случайная песня Rammstein",
        "/razrab - Фото разработчика",
        "/goida - 5 раз ГОЙДА",
        "/ban @username - Шуточный бан пользователя",
        "/unban @username - Снять шуточный бан",
        "/cactus - Отправить 3 кактуса",
        "",
        "<i>Для команд ban/unban можно отвечать на сообщение пользователя</i>"
    ]

    await update.message.reply_text("\n".join(commands), parse_mode="HTML")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("timeleft", timeleft))
    application.add_handler(CommandHandler("random", random_grade))
    application.add_handler(CommandHandler("Kreuzschlitzschraubendreher", kreuz_joke))
    application.add_handler(CommandHandler("BokuNoHero", boku_joke))
    application.add_handler(CommandHandler("rammstein", rammstein_song))

    application.add_handler(CommandHandler("razrab_down", razrab))
    application.add_handler(CommandHandler("goida", goida))
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(CommandHandler("unban", unban_user))
    application.add_handler(CommandHandler("cactus", send_cactus))
    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_banned_user
    ))

    application.run_polling()

if __name__ == "__main__":
    main()