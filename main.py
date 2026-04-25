import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
BOT_URL = os.getenv("RENDER_EXTERNAL_URL")  # Render сам подставит

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username or "нет_юзернейма"
    payload = " ".join(context.args) if context.args else "без_параметра"
    
    print(f"✅ Кликнул: @{username} | Параметр: {payload}")
    
    await update.message.reply_text(
        "Ничего не найдено.\n"
        "Эта ссылка недействительна."
    )

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Настраиваем webhook
    async def set_webhook():
        await application.bot.set_webhook(url=f"{BOT_URL}/webhook")

    # Flask маршрут для Telegram
    @app.route('/webhook', methods=['POST'])
    def webhook():
        update = Update.de_json(request.get_json(), application.bot)
        application.update_queue.put_nowait(update)
        return 'OK', 200

    @app.route('/')
    def index():
        return "Бот работает!"

    # Запуск
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(set_webhook())
    loop.run_until_complete(application.start())

    print(f"🤖 Бот запущен на webhook: {BOT_URL}/webhook")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if name == "__main__":
    main()
