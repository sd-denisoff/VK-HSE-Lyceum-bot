from config import *
import calendar
from datetime import datetime


def create_calendar():
    keyboard = VkKeyboard(one_time=True)
    now = datetime.now()
    keyboard.add_button(label=calendar.month_name[now.month] + ' ' + str(now.year), color=VkKeyboardColor.PRIMARY, payload={'action': 'title'})
    keyboard.add_line()
    for day in range(1, calendar.monthrange(now.year, now.month)[1] + 1):
        date = str(now.year) + str(now.month).zfill(2) + str(day).zfill(2)
        keyboard.add_button(label=str(day), color=VkKeyboardColor.DEFAULT, payload={'action': 'calendar', 'date': date})
        if day % 4 == 0:
            keyboard.add_line()
    return keyboard.get_keyboard()
