from flask import Flask, request, json
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


access_token = '5c494f5c880e7325a1f44ecebc85397b6bd65d24ff0d18416d554e83540a9ee8aac5204b5cf7e525ec225'
confirmation_token = 'c90019ed'

app = Flask(__name__)

session = vk_api.VkApi(token=access_token)
vk = session.get_api()
