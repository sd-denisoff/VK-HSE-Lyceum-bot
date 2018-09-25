from flask import Flask, request, json
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


APP_URL = 'https://28a59fe5.ngrok.io'

CSRF_ENABLED = False
WTF_CSRF_ENABLED = False
SECRET_KEY = '9)6odj22tkx_yxti%!$p*q!_k8eiw0z8bv2q)-y7zhg6*1^027'

app = Flask(__name__, template_folder='./web/templates', static_folder='./web/static')
app.config.from_object('config')


access_token = '5c494f5c880e7325a1f44ecebc85397b6bd65d24ff0d18416d554e83540a9ee8aac5204b5cf7e525ec225'
confirmation_token = 'c90019ed'

session = vk_api.VkApi(token=access_token)
vk = session.get_api()
