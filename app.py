import telebot
import requests
import base

bot = telebot.TeleBot(base.TOKEN)

OMDB_API_KEY = base.OMDB_API_KEY

print("Bot started...")

# State management: track what the user is searching for
user_state = {}


def search_movie(query, media_type="movie"):
    """Search OMDb API for a movie or series"""
    url = f"http://www.omdbapi.com/?t={query}&type={media_type}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data


def format_movie_info(data):
    """Format movie/series info into a nice message"""
    if data.get("Response") == "False":
        return "❌ متأسفانه چیزی پیدا نشد. لطفاً نام دیگه‌ای امتحان کن."

    title = data.get("Title", "-")
    year = data.get("Year", "-")
    genre = data.get("Genre", "-")
    imdb = data.get("imdbRating", "-")
    plot = data.get("Plot", "-")
    director = data.get("Director", "-")
    actors = data.get("Actors", "-")
    runtime = data.get("Runtime", "-")
    language = data.get("Language", "-")

    text = f"""
🎬 *{title}* ({year})

⏱ مدت زمان: {runtime}
🎭 ژانر: {genre}
🌍 زبان: {language}
🎥 کارگردان: {director}
👥 بازیگران: {actors}
⭐ امتیاز IMDb: {imdb}

📖 داستان:
{plot}
"""
    return text


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(
        message.chat.id,
        "🍿سلام! به بات معرفی فیلم و سریال خوش اومدی."
    )


@bot.message_handler(commands=['help', 'contact'])
def help_user(message):
    bot.reply_to(
        message,
        "📌برای استفاده از امکانات ربات از منوی اصلی کمک بگیر."
    )


@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup()

    btn1 = telebot.types.KeyboardButton("🎬جستجوی فیلم")
    btn2 = telebot.types.KeyboardButton("📺جستجوی سریال")
    btn3 = telebot.types.KeyboardButton("⭐فیلم‌های برتر")
    btn4 = telebot.types.KeyboardButton("🔥سریال‌های محبوب")
    btn5 = telebot.types.KeyboardButton("📞تماس با ما")
    btn6 = telebot.types.KeyboardButton("ℹ️درباره ما")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)

    bot.send_message(
        message.chat.id,
        "لطفاً یکی از گزینه‌های زیر را انتخاب کن:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: True)
def user_actions(message):
    chat_id = message.chat.id

    # ---- If user is in search mode ----
    if chat_id in user_state:
        media_type = user_state.pop(chat_id)
        bot.send_message(chat_id, "🔍 در حال جستجو...")
        data = search_movie(message.text, media_type)
        info = format_movie_info(data)

        # Send poster if available
        poster = data.get("Poster")
        if poster and poster != "N/A":
            bot.send_photo(chat_id, poster, caption=info, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, info, parse_mode="Markdown")
        return

    # ---- Menu buttons ----
    if message.text == "📞تماس با ما":
        email = "support@movies.com"
        phone = "09999632589"
        text = f"""
📬راه‌های ارتباطی

📧ایمیل: {email}

📱تلفن: {phone}
"""
        bot.send_message(chat_id, text)

    elif message.text == "ℹ️درباره ما":
        text = """
🎞 این ربات برای معرفی فیلم‌ها و سریال‌ها طراحی شده است.

🔎جستجو
⭐لیست‌های پیشنهادی
📚دسترسی سریع به اطلاعات مختلف
"""
        bot.send_message(chat_id, text)

    elif message.text == "🎬جستجوی فیلم":
        user_state[chat_id] = "movie"
        bot.send_message(chat_id, "🎥لطفاً نام فیلم موردنظر را وارد کن.")

    elif message.text == "📺جستجوی سریال":
        user_state[chat_id] = "series"
        bot.send_message(chat_id, "📺نام سریال موردنظر را وارد کنید.")

    elif message.text == "⭐فیلم‌های برتر":
        bot.send_message(chat_id, """
🏆فهرست فیلم‌های پیشنهادی:

1. The Godfather
2. Pulp Fiction
3. The Lord of the Rings
4. Seven
5. Interstellar
""")

    elif message.text == "🔥سریال‌های محبوب":
        bot.send_message(chat_id, """
🌟 فهرست سریال‌های محبوب:

1. Money Heist
2. The Last of Us
3. Wednesday
4. The Boys
5. Sherlock
""")


if __name__ == "__main__":
    bot.infinity_polling()
