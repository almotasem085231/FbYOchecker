import telebot
from telebot.types import InlineQueryResultArticle, InputTextMessageContent
from utils import ask_gemini
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 مرحباً! أرسل لي أي رسالة وسأجيبك .\n\n🤖 تم برمجتي بواسطة سوكونا.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if message.from_user.id == bot.get_me().id:
        return

    # يرد فقط إذا تم منشنه في القروبات
    if message.chat.type in ['group', 'supergroup']:
        if f"@{bot.get_me().username}" not in message.text:
            return

    prompt = message.text.replace(f"@{bot.get_me().username}", "").strip()
    response = ask_gemini(prompt)
    response += ""
    bot.reply_to(message, response)

@bot.inline_handler(func=lambda query: True)
def inline_query(inline_query):
    query_text = inline_query.query.strip()
    if not query_text:
        return

    try:
        response = ask_gemini(query_text)
        response += ""

        result = InlineQueryResultArticle(
            id="1",
            title="اضغط للحصول على الرد",
            input_message_content=InputTextMessageContent(response)
        )

        bot.answer_inline_query(inline_query.id, [result])
    except Exception as e:
        print("خطأ في inline mode:", e)

bot.infinity_polling()