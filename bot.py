import os
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from ali_express import AliExpressAPI
from phone_comparator import PhoneComparator
from storage import Storage
from constants import MESSAGES

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PhoneComparisonBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.ali_express = AliExpressAPI()
        self.phone_comparator = PhoneComparator()
        self.storage = Storage()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send welcome message when /start is issued."""
        welcome_msg = MESSAGES['welcome']
        keyboard = [
            [InlineKeyboardButton("مقارنة هواتف", callback_data='compare_phones')],
            [InlineKeyboardButton("البحث في AliExpress", callback_data='search_ali')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button presses."""
        query = update.callback_query
        await query.answer()

        if query.data == 'compare_phones':
            await query.message.reply_text(MESSAGES['enter_phones'])
            context.user_data['state'] = 'awaiting_phones'
        elif query.data == 'search_ali':
            await query.message.reply_text(MESSAGES['enter_product'])
            context.user_data['state'] = 'awaiting_product'

    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages."""
        state = context.user_data.get('state')

        if state == 'awaiting_phones':
            phones = update.message.text.split(',')
            if len(phones) != 2:
                await update.message.reply_text(MESSAGES['invalid_phones'])
                return

            comparison = self.phone_comparator.compare_phones(phones[0].strip(), phones[1].strip())
            await update.message.reply_text(comparison)
            context.user_data['state'] = None

        elif state == 'awaiting_product':
            product = update.message.text
            reviews = await self.ali_express.get_reviews(product)
            affiliate_link = await self.ali_express.get_affiliate_link(product)

            response = f"مراجعات المنتج:\n{reviews}\n\nرابط الشراء:\n{affiliate_link}"
            await update.message.reply_text(response)
            context.user_data['state'] = None

    def run(self):
        """Start the bot."""
        application = Application.builder().token(self.token).build()

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CallbackQueryHandler(self.button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))

        # Start the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Check if we have the bot token
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        print("Please set the TELEGRAM_BOT_TOKEN environment variable")
        exit(1)

    bot = PhoneComparisonBot()
    bot.run()