from flask import Flask, request, json
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


access_token = '5c494f5c880e7325a1f44ecebc85397b6bd65d24ff0d18416d554e83540a9ee8aac5204b5cf7e525ec225'
confirmation_token = 'c90019ed'

APP_URL = 'https://35afee79.ngrok.io'

CSRF_ENABLED = False
WTF_CSRF_ENABLED = False
SECRET_KEY = '9)6odj22tkx_yxti%!$p*q!_k8eiw0z8bv2q)-y7zhg6*1^027'

app = Flask(__name__, template_folder='./web/templates/')
app.config.from_object('config')

session = vk_api.VkApi(token=access_token)
vk = session.get_api()
