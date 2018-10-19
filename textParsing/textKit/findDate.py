import parsedatetime as pdt # $ pip install parsedatetime pyicu
import time
import datetime

class findDate:
    calendar = 0

    def __init__(self):
        self.calendar = pdt.Calendar(pdt.Constants(localeID='ru_RU'))

    def get_month_date(self, text):
        text_arr = text.split()

        for ind, word in enumerate(text_arr):
            if (word == 'неделю'):
                if (ind - 1 >= 0):
                    prev_word = text_arr[ind-1]
                    if (prev_word[:4] == 'пред'):
                        return 'prev_week'

                    elif (prev_word[:4] == 'след'):
                        return 'next_week'

                    else:
                        return 'this_week'

        return None


    def processNum(self, num):
        if (num < 9):
            return '0'+str(num)
        return str(num)

    def get(self, text):
        if (self.get_month_date(text) != None):
            return self.get_month_date(text)

        datetime_obj = self.calendar.parse(text)
        current_date = str(datetime_obj[0].tm_year) + self.processNum(datetime_obj[0].tm_mon) + self.processNum(datetime_obj[0].tm_mday)
        return current_date
