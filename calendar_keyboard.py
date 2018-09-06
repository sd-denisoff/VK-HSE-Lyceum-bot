from config import *
import calendar
from datetime import datetime


weekdays = {
    0: 'пн',
    1: 'вт',
    2: 'ср',
    3: 'чт',
    4: 'пт',
    5: 'сб',
    6: 'вс'
}


def create_calendar():
    keyboard = VkKeyboard(one_time=True)
    now = datetime.now()
    keyboard.add_button(label=calendar.month_name[now.month] + ' ' + str(now.year), color=VkKeyboardColor.PRIMARY, payload={'action': 'title'})
    keyboard.add_line()
    for day in range(1, calendar.monthrange(now.year, now.month)[1] + 1):
        date = str(now.year) + str(now.month).zfill(2) + str(day).zfill(2)
        weekday = weekdays[calendar.weekday(now.year, now.month, day)]
        keyboard.add_button(label=str(day) + ' ' + weekday, color=VkKeyboardColor.DEFAULT, payload={'action': 'calendar', 'date': date})
        if day % 4 == 0:
            keyboard.add_line()
    return keyboard.get_keyboard()
