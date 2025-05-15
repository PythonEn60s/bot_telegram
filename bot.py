import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
from flask import Flask
from threading import Thread

# Flask app para keep_alive
app = Flask('')

@app.route('/')
def home():
    return "Bot está corriendo!"

def run():
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# Variables de entorno
TOKEN = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "👋 Hola amigos!\n\n"
        "Bienvenidos al canal PythonEn60s, tu espacio para aprender Python de forma práctica y sencilla.\n\n"
        "Recuerden ser activos, compartir sus dudas y preguntar todo lo que quieran sobre Python o programación.\n"
        "Aquí estamos para ayudarnos entre todos.\n\n"
        "Para comenzar, escribe /help y descubre recursos y enlaces útiles.\n"
        "También síguenos en TikTok para más contenido: https://www.tiktok.com/@pythonen60seg\n"
        "Y no olvides la documentación oficial de Python: https://python.org/doc/\n"
    )
    await update.message.reply_text(mensaje)

# Comando /help con enlaces útiles
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🧠 <b>Recursos para aprender Python:</b>\n\n"
        "🐍 <a href='https://www.python.org/downloads/'>Descargar Python Oficial</a>\n"
        "📘 <a href='https://www.python.org/doc/'>Documentación oficial de Python</a>\n"
        "🎓 <a href='https://docs.python.org/es/3/tutorial/'>Tutorial oficial en español</a>\n"
        "💡 <a href='https://www.youtube.com/watch?v=mENHDQ8SLsI&list=PLyvsggKtwbLW1j0d5yaCkRF9Axpdlhsxz'>Aprende Python desde 0 (tutoriales prácticos)</a>\n"
        "📺 <a href='https://www.tiktok.com/@pythonen60seg'>Canal TikTok PythonEn60s</a>\n"
        "🧰 <a href='https://code.visualstudio.com/'>Descargar Visual Studio Code</a>\n"
    )
    await update.message.reply_html(help_text, disable_web_page_preview=True)

# Bienvenida a nuevos miembros con mención
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        mention = f"<a href='tg://user?id={member.id}'>{member.first_name}</a>"
        await update.message.reply_html(
            f"🎉👋 ¡Hola {mention}! 🎈\n"
            f"Nos alegra mucho que te unas al grupo PythonEn60s 🐍✨.\n"
            f"🚀 Aquí aprenderás y compartirás todo sobre Python 💻📚.\n"
            f"💬 No dudes en presentarte y hacer tus preguntas ❓🧓.\n"
            f"¡Bienvenido/a! 🎊🎉"
        )

# Mensaje programado para activar el grupo, versión asíncrona para apscheduler
async def enviar_mensaje():
    await bot.send_message(chat_id=GROUP_ID, text="📢 ¡Gracias por formar parte de la comunidad PythonEn60s, No olvides compartir tus dudas, tips o avances en Python! 🐍📋")

def job():
    asyncio.create_task(enviar_mensaje())

# Crear bot y aplicación
bot = Bot(TOKEN)
app_telegram = ApplicationBuilder().token(TOKEN).build()

# Programar tarea cada 2 horas (usando job síncrono que lanza tarea asíncrona)
scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', hours=2)
scheduler.start()

# Agregar handlers
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CommandHandler("help", help_command))
app_telegram.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

# Ejecutar keep_alive y bot
if __name__ == '__main__':
    keep_alive()
    app_telegram.run_polling()
