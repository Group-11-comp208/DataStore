import websocket
from database import Database
import json
import time
import requests
import telegram
from fx import Converter
import coincap

try:
    import thread
except ImportError:
    import _thread as thread


class CoinCapWebSocket:
    def __init__(self):
        self.database = Database()
        self.converter = Converter()
        self.coincap = coincap.CoinCap()
        self.connect()

    def connect(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://ws.coincap.io/prices?assets=ALL",
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        ws.run_forever()

    def on_message(self, ws, message):
        response = json.loads(message)
        for key, value in response.items():
            t = time.time() * 1000
            try:
                current_price = self.database.get_price(key)
                change = ((float(value) - current_price)/current_price) * 100
                if abs(change) >= 1:
                    print("Updating price for {}".format(key))
                    self.database.update_or_insert_crypto(key, value, t)
                    chats = self.database.should_update(key)
                    for chat in chats:
                        self.telegram_bot_sendtext(chat, key, change, value)
            except IndexError:
                print("Inserting new price for {}".format(key))
                self.database.update_or_insert_crypto(key, value, t)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")
        time.sleep(15)
        # Restart connection
        self.connect()

    def on_open(self, ws):
        def run(*args):
            while True:
                time.sleep(5)
            time.sleep(1)
            ws.close()
            print("thread terminating...")
        thread.start_new_thread(run, ())

    def telegram_bot_sendtext(self, chatID, asset, change, value):
        bot = telegram.Bot(
            token='1543822532:AAEQJRD2-diWs0hCUSrVA8KqlDYkg-NV0_0')
        currency = self.database.get_currency(chatID)
        currency_symbol = self.converter.get_symbol(currency)
        name = self.coincap.get_asset(asset)['name']
        rate = 1
        if currency != "usd":
            rate = self.converter.get_rate(currency)
        text = ""
        if (change > 0):
            text = "up"
        else:
            text = "down"
        bot.sendMessage(chat_id=chatID, text="*Price alert*\n{} is {} by {:.2f}% \nCurrent Price: {}{:.2f}".format(
            name, text, change, currency_symbol, float(value) * rate), parse_mode=telegram.ParseMode.MARKDOWN)


web = CoinCapWebSocket()
