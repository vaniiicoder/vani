import telebot
import base

bot = telebot.TeleBot(base.TOKEN)

print("Bot started...")


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

    if message.text == "📞تماس با ما":

        email = "support@movies.com"
        phone = "09999632589"

        text = f"""
📬راه‌های ارتباطی

📧ایمیل: {email}

📱تلفن: {phone}
"""

        bot.send_message(message.chat.id, text)

    elif message.text == "ℹ️درباره ما":

        text = """
🎞 این ربات برای معرفی فیلم‌ها و سریال‌ها طراحی شده است.

🔎جستجو
⭐لیست‌های پیشنهادی
📚دسترسی سریع به اطلاعات مختلف
"""

        bot.send_message(message.chat.id, text)

    elif message.text == "🎬جستجوی فیلم":

        bot.send_message(
            message.chat.id,
            "🎥لطفاً نام فیلم موردنظر را وارد کن."
        )

    elif message.text == "📺جستجوی سریال":

        bot.send_message(
            message.chat.id,
            "📺نام سریال موردنظر را وارد کنید."
        )

    elif message.text == "⭐فیلم‌های برتر":

        bot.send_message(
            message.chat.id,
            """
🏆فهرست فیلم‌های پیشنهادی:

1. The Godfather
2. Pulp Fiction
3. The Lord of the Rings
4. Seven
5. Interstellar
"""
        )

    elif message.text == "🔥سریال‌های محبوب":
        bot.send_message(
            message.chat.id,
            """
🌟 فهرست سریال‌های محبوب:

1. Money Heist
2. The Last of Us
3. Wednesday
4. The Boys
5. Sherlock
"""
        )


if __name__ == "__main__":
    bot.infinity_polling()