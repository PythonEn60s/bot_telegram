from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

# Token del bot
TOKEN = '7881078584:AAFh90GNIEkeJrX9CM9lvxq16SbiQyU2Xyk'
# Reemplaza este ID con el ID real de tu grupo (usa @userinfobot para obtenerlo)
GROUP_ID = -2510330599

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "👋 Hola amigos!\n\n"
        "Bienvenidos al canal PythonEn60s, tu espacio para aprender Python de forma práctica y sencilla.\n\n"
        "Recuerden ser activos, compartir sus dudas y preguntar todo lo que quieran sobre Python o programación.\n"
        "Aquí estamos para ayudarnos entre todos.\n\n"
        "Para comenzar, escribe /help y descubre recursos y enlaces útiles.\n"
        "También síguenos en TikTok para más contenido: https://www.tiktok.com/@pythonen60seg\n"
        "Y no olvides la documentación oficial de Python: https://www.python.org/doc/\n"
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

# Mensaje programado para activar el grupo
async def enviar_mensaje():
    await bot.send_message(chat_id=GROUP_ID, text="📢 ¡Gracias por formar parte de la comunidad PythonEn60s, No olvides compartir tus dudas, tips o avances en Python! 🐍📋")

# Crear bot y aplicación
bot = Bot(TOKEN)
app = ApplicationBuilder().token(TOKEN).build()

# Programar tarea cada 2 horas
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: asyncio.run(enviar_mensaje()), 'interval', hours=2)
scheduler.start()

# Agregar handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

# Ejecutar el bot
app.run_polling()
