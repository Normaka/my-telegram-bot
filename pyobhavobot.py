import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
import math

# Telegram bot tokenini o'zgartiring
TOKEN = '6068134146:AAE39Tu_o8giS9zHEz7NXvpEAigfL9UmLu8'

# Log yozish uchun sozlamalar
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# /start komandasi uchun funksiyaning yozilishi
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Salom! Men kalkulyator botiman. Menga arifmetik ifodalarni yuboring, men ularni hisoblab beraman.")


# Kalkulyator funksiyasi (arifmetik ifodani baholash)
async def calculate(update: Update, context: CallbackContext):
    try:
        # Foydalanuvchi yuborgan ifodani olish
        expression = update.message.text
        # Ifodani baholash va natijani qaytarish
        result = eval(expression)
        await update.message.reply_text(f"Natija: {result}")
    except Exception as e:
        # Xatolik bo'lsa, xabar yuborish
        await update.message.reply_text("Xatolik yuz berdi. Iltimos, faqat arifmetik ifodalar yuboring.")
        logger.error(f"Error evaluating expression: {e}")


# Xatoliklarni qayta ishlash
def error(update: Update, context: CallbackContext):
    logger.warning(f"Update {update} caused error {context.error}")


# Botni ishga tushurish
def main():
    # Application ob'ekti yaratish
    application = Application.builder().token(TOKEN).build()

    # /start komandasini qo'shish
    application.add_handler(CommandHandler("start", start))

    # Barcha xabarlarni olish va hisoblash uchun handler qo'shish
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))  # filters TEXT ni ishlatish

    # Xatoliklarni qayta ishlash
    application.add_error_handler(error)

    # Botni ishga tushurish
    application.run_polling()


if __name__ == '__main__':
    main()
