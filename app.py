import telebot
import requests
import base

bot = telebot.TeleBot(base.TOKEN)
OMDB_API_KEY = base.OMDB_API_KEY

print("Bot started...")

# Track user state: what command they used last
user_state = {}


def get_movie_by_id(imdb_id):
    """Search OMDb by IMDb ID (e.g. tt0110912)"""
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json()


def get_movie_by_name(name, media_type="movie"):
    """Search OMDb by title"""
    url = f"http://www.omdbapi.com/?t={name}&type={media_type}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json()


def format_movie_info(data):
    """Format OMDb result into a readable message"""
    if data.get("Response") == "False":
        return "❌ متأسفانه چیزی پیدا نشد. لطفاً دوباره امتحان کن."

    title    = data.get("Title", "-")
    year     = data.get("Year", "-")
    genre    = data.get("Genre", "-")
    imdb_r   = data.get("imdbRating", "-")
    imdb_id  = data.get("imdbID", "-")
    plot     = data.get("Plot", "-")
    director = data.get("Director", "-")
    actors   = data.get("Actors", "-")
    runtime  = data.get("Runtime", "-")
    language = data.get("Language", "-")
    mtype    = data.get("Type", "-")

    return f"""
🎬 *{title}* ({year})

🆔 IMDb ID: `{imdb_id}`
🎭 نوع: {mtype}
⏱ مدت زمان: {runtime}
🎞 ژانر: {genre}
🌍 زبان: {language}
🎥 کارگردان: {director}
👥 بازیگران: {actors}
⭐ امتیاز IMDb: {imdb_r}

📖 داستان:
{plot}
"""


def send_result(chat_id, data):
    """Send poster + info or just info"""
    info = format_movie_info(data)
    poster = data.get("Poster")
    if poster and poster != "N/A":
        bot.send_photo(chat_id, poster, caption=info, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, info, parse_mode="Markdown")


# ───────────────────────── Commands ─────────────────────────

@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(
        message.chat.id,
        "🍿 سلام! به بات معرفی فیلم و سریال خوش اومدی.\n\n"
        "دستورهای موجود:\n"
        "/menu — منوی اصلی\n"
        "/moviename — جستجو با نام فیلم\n"
        "/movieid — جستجو با آی‌دی IMDb\n"
        "/help — راهنما"
    )


@bot.message_handler(commands=['help', 'contact'])
def help_user(message):
    bot.reply_to(
        message,
        "📌 دستورهای ربات:\n\n"
        "/moviename — نام فیلم یا سریال را وارد کن\n"
        "/movieid — آی‌دی IMDb را وارد کن (مثلاً tt0110912)\n"
        "/menu — منوی اصلی\n"
    )


@bot.message_handler(commands=['moviename'])
def ask_movie_name(message):
    user_state[message.chat.id] = 'moviename'
    bot.send_message(message.chat.id, "🎬 نام فیلم یا سریال موردنظر را بنویس:")


@bot.message_handler(commands=['movieid'])
def ask_movie_id(message):
    user_state[message.chat.id] = 'movieid'
    bot.send_message(
        message.chat.id,
        "🆔 آی‌دی IMDb فیلم را وارد کن:\n"
        "_(مثلاً: tt0110912)_",
        parse_mode="Markdown"
    )


@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("🎬جستجوی فیلم"),
               telebot.types.KeyboardButton("📺جستجوی سریال"))
    markup.add(telebot.types.KeyboardButton("⭐فیلم‌های برتر"),
               telebot.types.KeyboardButton("🔥سریال‌های محبوب"))
    markup.add(telebot.types.KeyboardButton("📞تماس با ما"),
               telebot.types.KeyboardButton("ℹ️درباره ما"))

    bot.send_message(
        message.chat.id,
        "لطفاً یکی از گزینه‌های زیر را انتخاب کن:",
        reply_markup=markup
    )


# ───────────────────────── Text handler ─────────────────────────

@bot.message_handler(func=lambda message: True)
def user_actions(message):
    chat_id = message.chat.id
    text = message.text

    # Handle pending state from /moviename or /movieid
    if chat_id in user_state:
        state = user_state.pop(chat_id)

        if state == 'moviename':
            bot.send_message(chat_id, "🔍 در حال جستجو...")
            data = get_movie_by_name(text)
            send_result(chat_id, data)

        elif state == 'movieid':
            bot.send_message(chat_id, "🔍 در حال جستجو...")
            # Accept with or without 'tt' prefix
            imdb_id = text.strip()
            if imdb_id.isdigit():
                imdb_id = "tt" + imdb_id.zfill(7)
            data = get_movie_by_id(imdb_id)
            send_result(chat_id, data)
        return

    # Menu keyboard buttons
    if text == "📞تماس با ما":
        bot.send_message(chat_id,
            "📬 راه‌های ارتباطی\n\n📧 ایمیل: support@movies.com\n📱 تلفن: 09999632589")

    elif text == "ℹ️درباره ما":
        bot.send_message(chat_id,
            "🎞 این ربات برای معرفی فیلم‌ها و سریال‌ها طراحی شده است.\n\n"
            "🔎 جستجو\n⭐ لیست‌های پیشنهادی\n📚 دسترسی سریع به اطلاعات")

    elif text == "🎬جستجوی فیلم":
        user_state[chat_id] = 'moviename'
        bot.send_message(chat_id, "🎥 لطفاً نام فیلم موردنظر را وارد کن.")

    elif text == "📺جستجوی سریال":
        user_state[chat_id] = 'moviename'
        bot.send_message(chat_id, "📺 نام سریال موردنظر را وارد کنید.")

    elif text == "⭐فیلم‌های برتر":
        bot.send_message(chat_id,
            "🏆 فهرست فیلم‌های پیشنهادی:\n\n"
            "1. The Godfather\n2. Pulp Fiction\n3. The Lord of the Rings\n"
            "4. Seven\n5. Interstellar")

    elif text == "🔥سریال‌های محبوب":
        bot.send_message(chat_id,
            "🌟 فهرست سریال‌های محبوب:\n\n"
            "1. Money Heist\n2. The Last of Us\n3. Wednesday\n"
            "4. The Boys\n5. Sherlock")


if __name__ == "__main__":
    bot.infinity_polling()
