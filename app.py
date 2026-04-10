from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
import threading
import random
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)
CORS(app)

bots = {}
running = {}
last_promo = {}

EMOJIS = ["❤️","🔥","😂","😍","👍"]

PROMO_TEXT = "🚀 Powered by Muskan Bot Panel\n💡 Apna bot yaha bana sakte ho"
WEBSITE_LINK = "https://YOUR-VERCEL-LINK.vercel.app"  # 👈 change this

def run_bot(token):
    bot = telebot.TeleBot(token)
    running[token] = True
    last_promo[token] = datetime.now()

    @bot.message_handler(func=lambda m: True)
    def react(message):
        if not running.get(token):
            return

        try:
            # 🔥 Auto Reaction
            emoji = random.choice(EMOJIS)
            bot.send_reaction(message.chat.id, message.message_id, emoji)

            # 🎯 Promo only in private chat (1 time in 24h)
            if message.chat.type == "private":
                now = datetime.now()

                if now - last_promo[token] > timedelta(hours=24):

                    markup = InlineKeyboardMarkup()
                    btn = InlineKeyboardButton(
                        "🌐 Visit Website",
                        url=WEBSITE_LINK
                    )
                    markup.add(btn)

                    bot.send_message(
                        message.chat.id,
                        PROMO_TEXT,
                        reply_markup=markup
                    )

                    last_promo[token] = now

        except:
            pass

    bot.infinity_polling()

@app.route("/start", methods=["POST"])
def start():
    token = request.json.get("token")

    if token in bots:
        return jsonify({"msg": "Already Running"})

    t = threading.Thread(target=run_bot, args=(token,))
    t.start()

    bots[token] = t
    return jsonify({"msg": "Bot Started"})

@app.route("/stop", methods=["POST"])
def stop():
    token = request.json.get("token")

    if token in running:
        running[token] = False
        return jsonify({"msg": "Bot Stopped"})

    return jsonify({"msg": "Bot Not Found"})

@app.route("/")
def home():
    return "✅ Bot Server Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)