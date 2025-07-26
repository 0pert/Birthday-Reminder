from bday.utils import today, time_str_to_obj


class Person:
    def __init__(self, name, date_of_birth):
        self.name = name
        self.date_of_birth = time_str_to_obj(date_of_birth)
        self.birthday, self.age = self.get_age()

    def get_age(self):
        todays_date = today()
        age = todays_date.year - self.date_of_birth.year

        if (todays_date.month, todays_date.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1

        birthday = self.date_of_birth.strftime("%d %B")
        return birthday, age + 1

