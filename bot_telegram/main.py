"""Punto de entrada del bot de Telegram de BodyMap."""
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot_telegram.config import BOT_TOKEN
from bot_telegram.responses import get_response

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MENSAJE_INICIO = (
    "Hola, soy el bot asistente de BodyMap. ¿Cómo estás? "
    "Escribime qué zona del cuerpo te molesta (cabeza, cuello, espalda, "
    "abdomen, brazos o piernas) para darte orientación general."
)

MENSAJE_AYUDA = (
    'Podés escribirme directamente tu molestia, por ejemplo: "dolor de cabeza", '
    '"me duele la espalda" o "molestia en el cuello". '
    "También podés visitar nuestro mapa corporal interactivo en la web de BodyMap."
)

MENSAJE_ZONAS = (
    "Zonas disponibles para consulta rápida en BodyMap:\n"
    "- Cabeza\n- Cuello\n- Pecho\n- Abdomen\n- Brazos\n- Piernas\n"
    "Escribí el nombre de cualquiera de estas zonas para recibir información."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENSAJE_INICIO)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENSAJE_AYUDA)


async def zonas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENSAJE_ZONAS)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text or ""
    logger.info("Mensaje de %s: %s", update.message.chat.id, texto)
    await update.message.reply_text(get_response(texto))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Error al procesar un update: %s", context.error)


def main():
    if not BOT_TOKEN:
        raise SystemExit(
            "Falta TELEGRAM_TOKEN. Copiá .env.example a .env y pegá "
            "el token entregado por @BotFather."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("zonas", zonas))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.add_error_handler(error_handler)

    logger.info("Bot de BodyMap iniciado")
    application.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()
