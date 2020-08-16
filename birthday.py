import discord
from datetime import datetime, time, timedelta
import random
import dateparser

class Birthdays():

    def __init__(self):
        with open("birthdays.txt") as fp:
            tmp = [line.strip() for line in fp.readlines()]
            self.all_birthdays = [self.Birthday(l).get_birthday() for l in tmp]
        self.all_birthdays.sort(key=lambda Birthday: Birthday.time_till)

    class Birthday():

        def __init__(self, data):
            data_split = data.split(":-:")
            self.user_id = int(data_split[0])
            self.user_display_name = data_split[1]
            self.user_birthday = dateparser.parse(data_split[2])
            self.time_till = self.days_till_birthday()
            self.birthday_string = self.user_birthday.strftime("%B %-d")

        def get_birthday(self):
            return self

        def days_till_birthday(self):
            now = datetime.now()
            if self.user_birthday < now:
                self.user_birthday = datetime(self.user_birthday.year + 1, self.user_birthday.month, self.user_birthday.day)
            return (self.user_birthday - now).days
