import json
from bday.person import Person
from bday.utils import today


class BdayList:
    """ List of Person objects """
    def __init__(self):
        self.people = []
        self.today = today()
        self.today_str = self.today.strftime("%d %B - %Y")

    def add(self, name, birth_date):
        person = Person(name, birth_date)
        self.people.append(person)

    def remove(self, name):
        for person in self.people:
            if person.name == name:
                self.people.remove(person)

    @classmethod
    def from_json(cls):
        new_bday_list = cls()

        with open("data.json", "r") as fhand:
            data = json.load(fhand)

        for person in data:
            new_bday_list.add(person, data[person]["date_of_birth"])

        return new_bday_list

    def save_to_file(self):
        data = {}
        for person in self.people:
            data[person.name] = {
                "date_of_birth": str(person.date_of_birth)[:11]
            }
       
        with open("data.json", "w", encoding="UTF-8") as fhand:
            fhand.write(json.dumps(data, indent=2,))

    def sort_dates(self):
        """
        Sorting self.people based on todays date.
        """
        self.people.sort(key=lambda person: (person.date_of_birth.month, person.date_of_birth.day))
        pre_today = []
        post_today = []
        for person in self.people:
            if (person.date_of_birth.month, person.date_of_birth.day) < (self.today.month, self.today.day):

                pre_today.append(person)
            else:
                post_today.append(person)
        new_list = post_today + pre_today

        self.people = new_list
