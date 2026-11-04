from abc import ABC, abstractmethod
from operator import index

P = 10


def whole_number(value, minimum, maximum=None):
    try:
        number = index(value)
    except TypeError:
        raise ValueError("A whole number is required") from None

    if value is True or value is False:
        raise ValueError("A whole number is required")

    if number < minimum or (maximum is not None and number > maximum):
        raise ValueError("Number is outside the allowed range")

    return number


# Question 1: Clock and people

class Clock:
    def __init__(self, hour=0):
        self.set_hour(hour)

    def now(self):
        return self.__hour

    def set_hour(self, hour):
        self.__hour = whole_number(hour, 0, 168)


class Person(ABC):
    constructor_count = 0

    def __init__(self, name, person_id, **kwargs):
        super().__init__(**kwargs)

        if not name or not name.strip():
            raise ValueError("Name cannot be empty")

        self.__name = name.strip()
        self.__id = whole_number(person_id, 1)
        Person.constructor_count += 1

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @abstractmethod
    def role(self):
        pass


class Patient(Person):
    def role(self):
        return "Patient"

    def can_book_as_patient(self):
        return True

