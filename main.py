import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

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
    
    print("🤖 Бот запущен и ожидает кликов...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if name == "__main__":
    main()
