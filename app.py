import os
import logging
import signal
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import requests

# Конфигурация из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Константы
MAX_RADIUS = 5000
MIN_RADIUS = 100
RADIUS, LOCATION = range(2)

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(name)

class CafeBot:
    def init(self):
        self.updater = Updater(TOKEN, use_context=True)
        self.session = requests.Session()

    # ... (остальные методы из предыдущего кода без изменений)

    def run(self):
        """Запуск бота с вебхуками"""
        dispatcher = self.updater.dispatcher

        # Регистрация обработчиков
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('findcafe', self.find_cafe)],
            states={
                RADIUS: [MessageHandler(Filters.text & ~Filters.command, self.receive_radius)],
                LOCATION: [MessageHandler(Filters.location, self.receive_location)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )

        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(conv_handler)

        # Настройка вебхуков
        self.updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
        )

        logger.info("🤖 Бот запущен с вебхуками...")
        self.updater.idle()

if name == 'main':
    bot = CafeBot()
    bot.run()
