from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import calendar


def create_calendar(year, month):
    markup = InlineKeyboardMarkup()

    row = list()
    row.append(InlineKeyboardButton(calendar.month_name[month] + ' ' + str(year), callback_data='ignore'))
    markup.row(*row)

    row.clear()
    week_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    for day in week_days:
        row.append(InlineKeyboardButton(day, callback_data='ignore'))
    markup.row(*row)

    user_calendar = calendar.monthcalendar(year, month)
    for week in user_calendar:
        row.clear()
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(' ', callback_data='ignore'))
            else:
                row.append(InlineKeyboardButton(str(day), callback_data='day-' + str(day)))
        markup.row(*row)

    row.clear()
    row.append(InlineKeyboardButton('<<', callback_data='previous-month'))
    row.append(InlineKeyboardButton(' ', callback_data='ignore'))
    row.append(InlineKeyboardButton('>>', callback_data='next-month'))
    markup.row(*row)

    return markup
