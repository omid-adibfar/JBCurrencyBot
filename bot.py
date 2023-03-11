import telebot
import datetime

from logger import get_logger
from alan_chand import buy_price, sell_price
from alan_chand import (
    aed_target_url as AED,
    usd_target_url as USD,
    usd_remittance_target_url as USDR,
    eu_target_url as EUR,
    eu_remittance_target_url as EURR,
    pound_target_url as POUND,
    cad_target_url as CAD,
    cny_target_url as CNY,
    aud_target_url as AUD
)
from decouple import config
from apscheduler.schedulers.background import BackgroundScheduler


BOT_TOKEN = config('BOT_TOKEN')
BOT_CHAT_ID = config('BOT_CHAT_ID')
CHANNEL_CHAT_ID = config('CHANNEL_CHAT_ID')
CHANNEL_EDITABLE_MESSAGE_ID = config('CHANNEL_EDITABLE_MESSAGE_ID', cast=int)
UPDATE_INTERVAL = config('UPDATE_INTERVAL', cast=int)

bot = telebot.TeleBot(BOT_TOKEN)

logger = get_logger()

logger.debug("Bot restarted with following configs (CHANNEL_EDITABLE_MESSAGE_ID={}, UPDATE_INTERVAL={} seconds)".format(
    CHANNEL_EDITABLE_MESSAGE_ID, UPDATE_INTERVAL))


class Message:
    def __init__(self, id) -> None:
        self.id = id


msg = Message(CHANNEL_EDITABLE_MESSAGE_ID)


def get_command_details():
    return "\n\n/help - Get help\n/update - Get latest price of currencies and converts them to IRR"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.debug("Bot started.")
    try:
        bot.reply_to(
            message, "Welcome to JB Currencies Rate Bot, Please select one of the options below:" + get_command_details())
    except Exception as e:
        logger.error('An Exception Occurred', exc_info=e)


@bot.message_handler(commands=['help'])
def send_help(message):
    logger.debug("Help command executed.")
    try:
        bot.reply_to(
            message, "Please select one of the options below to continue:" + get_command_details())
    except Exception as e:
        logger.error('An Exception Occurred', exc_info=e)


@bot.message_handler(commands=['update'])
def update_prices(message):
    logger.debug("Update command executed.")
    if msg.id == -1:
        bot.send_message(CHANNEL_CHAT_ID, "GETTING LATEST PRICE...")
        msg.id = CHANNEL_EDITABLE_MESSAGE_ID
    try:
        bot.edit_message_text(chat_id=CHANNEL_CHAT_ID,
                              text="""
                            {}

    درهم امارات🇦🇪 خريد: {}🔹فروش: {}
    |
    دلار امریکا🇺🇸 خريد: {}🔹فروش: {}
    |
    حواله دلار🇺🇸 خريد: {}🔹فروش: {}
    |
    یورو🇪🇺 خريد: {}🔹فروش: {}
    |
    حواله یورو🇪🇺 خريد: {}🔹فروش: {}
    |
    پوند انگلیس🇪🇺 خريد: {}🔹فروش: {}
    |
    دلار کانادا🇨🇦 خريد: {}🔹فروش: {}
    |
    یوان چین🇨🇳 خريد: {}🔹فروش: {}
    |
    دلار استرالیا🇦🇺 خريد: {}🔹فروش: {}
    |
                            """.format(
                                  datetime.datetime.now().strftime(
                                      "%#d %b"),  # use hyphen instead of hashtag in Unix systems to skip zero
                                  buy_price(AED), sell_price(AED),
                                  buy_price(USD), sell_price(USD),
                                  buy_price(USDR), sell_price(USDR),
                                  buy_price(EUR), sell_price(EUR),
                                  buy_price(EURR), sell_price(EURR),
                                  buy_price(POUND), sell_price(POUND),
                                  buy_price(CAD), sell_price(CAD),
                                  buy_price(CNY), sell_price(CNY),
                                  buy_price(AUD), sell_price(AUD),
                              ), message_id=msg.id)
    except Exception as e:
        logger.error('An Exception Occurred', exc_info=e)


def auto_update():
    try:
        sched = BackgroundScheduler()
        sched.add_job(update_prices, 'interval', args=[
            None, ], seconds=UPDATE_INTERVAL)
        sched.start()
    except Exception as e:
        logger.error('An Exception Occurred', exc_info=e)


try:
    auto_update()
    bot.infinity_polling()
except Exception as e:
    logger.error('An Exception Occurred', exc_info=e)
