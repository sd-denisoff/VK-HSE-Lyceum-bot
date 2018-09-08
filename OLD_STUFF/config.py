import telebot
import flask

# token = '419371540:AAEp0CCiQQ_NHUIbMSJHSGQixD0stHL_YT0'

token = '410664025:AAHoMEoGy5itvap9CwVVdmf3HC4xYvTSiQY'
bot = telebot.AsyncTeleBot(token)

WEBHOOK_HOST = 'eb84e3ca.ngrok.io'
WEBHOOK_PORT = 8080
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './cert.pem'
WEBHOOK_SSL_PRIV = './priv.pem'

app = flask.Flask(__name__)

bot.remove_webhook()
bot.set_webhook(url='https://' + WEBHOOK_HOST + ':' + str(WEBHOOK_PORT) + '/' + token + '/',
               certificate=open(WEBHOOK_SSL_CERT, 'r'))
