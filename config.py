from flask import Flask, request, json
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from textParsing.brain import brain

APP_URL = 'https://ff97e10e.ngrok.io'

CSRF_ENABLED = False
WTF_CSRF_ENABLED = False
SECRET_KEY = '9)6odj22tkx_yxti%!$p*q!_k8eiw0z8bv2q)-y7zhg6*1^027'

app = Flask(__name__, template_folder='./web/templates', static_folder='./web/static')
app.config.from_object('config')


access_token = '399659d138040fdb53eeab9ad01bf6ca33c29666500507b4fecc0079c2e6397cf3a8f33c16b7af140d8f0'
confirmation_token = '203d5b48'

session = vk_api.VkApi(token=access_token)
vk = session.get_api()

b = brain()
