from collections import UserDict
from datetime import datetime
import json


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def save(self):
        # writing data to a file
        with open('filename.json', 'w') as file:
            json.dump(self.to_dict(), file, indent=4)
            print("Users saved.")

    def to_dict(self):
        # add data to dict
        return {
            name: record.to_dict() for name, record in self.data.items()
        }

    def load(self):
        # get dictionary from json file
        with open('filename.json', 'r') as file:
            data = json.load(file)
            self.data = {
                name: Record(
                    Name(record_data['name']),
                    Phone(record_data['phones'][0]) if record_data['phones'] else None,
                    Birthday(datetime.strptime(record_data['birthday'], '%Y-%m-%d')) if record_data[
                        'birthday'] else None
                )
                for name, record_data in data.items()
            }
            print("Data loaded from file.")

    def iterator(self, n):
        count = 0
        for record in self.data.values():
            yield record
            count += 1
            if count >= n:
                return

    def search(self):
        # search values by keywords
        keyword = input('Input keyword: ')
        results = []
        for record in self.data.values():
            # convert to lower case to compare the entered keyword among values
            # add value to list if True
            if keyword.lower() in record.name.value.lower() or any(
                    keyword.lower() in phone.value.lower()[:len(keyword)] for phone in record.phones
            ):
                results.append(record)

        if results:
            print("Search results:")
            for result in results:
                print(f"Name: {result.name.value}")
                for phone in result.phones:
                    print(f"Phone: {phone.value}")
                if result.birthday:
                    print(f"Birthday: {result.birthday.value.strftime('%Y-%m-%d')}")
        else:
            print("No results found.")
        return results


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [] if phone is None else [phone]
        self.birthday = birthday

    def to_dict(self):
        # make dict of phone and birthday
        return {
            'name': self.name.value,
            'phones': [phone.value for phone in self.phones] if self.phones else None,
            'birthday': self.birthday.value.strftime('%Y-%m-%d') if self.birthday else None
        }

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index_of_old_phone = self.phones.index(old_phone)
        self.phones[index_of_old_phone] = new_phone

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            return (next_birthday - today).days


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    pass


class Phone(Field):

    @property
    def correct_phone(self):
        return self.__value

    @correct_phone.setter
    def correct_phone(self, value):
        if not isinstance(value, str):
            raise ValueError("Phone number must be a string")
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number")
        self.__value = value


class Birthday(Field):

    @property
    def correct_birthday(self):
        return self.__value

    @correct_birthday.setter
    def correct_birthday(self, value):
        if not isinstance(value, datetime):
            raise ValueError("Birthday must be a datetime object")
        self.__value = value


if __name__ == '__main__':
    ab = AddressBook()
    ab.add_record(Record(Name("Alice"), Phone("1111111111"), Birthday(datetime(1990, 5, 17))))
    ab.add_record(Record(Name("Bob"), Phone("2222222222")))
    ab.save()
    ab.load()
    ab.search()
