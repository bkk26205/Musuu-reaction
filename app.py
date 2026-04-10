import telebot
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

running_bots = {}

def run_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(msg):
        bot.send_message(msg.chat.id, "✅ Bot Active! Send any message")

    @bot.message_handler(func=lambda m: True)
    def react(message):
        try:
            bot.send_message(message.chat.id, "🔥 Reaction working!")
            print("Message received:", message.text)
        except Exception as e:
            print("Error:", e)

    print("Bot polling started...")
    bot.infinity_polling(skip_pending=True)

@app.route("/start", methods=["POST"])
def start_bot():
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"msg": "Token missing"})

    if token in running_bots:
        return jsonify({"msg": "Already running"})

    try:
        t = threading.Thread(target=run_bot, args=(token,))
        t.daemon = True
        t.start()

        running_bots[token] = True
        return jsonify({"msg": "Bot started successfully"})
    
    except Exception as e:
        return jsonify({"msg": str(e)})

@app.route("/")
def home():
    return "Backend Running!"
