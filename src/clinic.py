from abc import ABC, abstractmethod
from contextlib import contextmanager
from enum import Enum
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


# Question 3: Polymorphism and fees

class Staff(Person):
    @abstractmethod
    def fee(self):
        pass

    @abstractmethod
    def bufferHours(self):
        pass

    def can_book_as_staff(self):
        return True


class Doctor(Staff):
    def role(self):
        return "Doctor"

    def fee(self):
        return 40 + 5 * (P % 5)

    def bufferHours(self):
        return 2


class Nurse(Staff):
    def role(self):
        return "Nurse"

    def fee(self):
        return 10 + (P % 3)

    def bufferHours(self):
        return 1


class Pharmacist(Staff):
    def role(self):
        return "Pharmacist"

    def fee(self):
        return 5

    def bufferHours(self):
        return 0


# Question 5: Multiple inheritance

class Lecturer(Person):
    def __init__(self, name, person_id, module, **kwargs):
        if not module or not module.strip():
            raise ValueError("Module cannot be empty")

        self.__module = module.strip()
        super().__init__(name, person_id, **kwargs)

    @property
    def module(self):
        return self.__module

    def role(self):
        return "Lecturer"


class MedicalLecturer(Doctor, Lecturer):
    def __init__(self, name, person_id, module):
        super().__init__(name, person_id, module=module)

    def role(self):
        return "Doctor and Lecturer"


# Question 2: Appointment statuses

class Status(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


# Appointment invariants:
# ID is positive; start hour is an integer from 0 to 167.
# Every appointment lasts one hour and has a valid patient and staff member.
# Status is PENDING, CONFIRMED or CANCELLED; CANCELLED is final.

class Appointment:
    def __init__(self, appointment_id, patient, staff, start_hour):
        self.__id = whole_number(appointment_id, 1)
        self.__start_hour = whole_number(start_hour, 0, 167)

        if not callable(getattr(patient, "can_book_as_patient", None)) or not patient.can_book_as_patient():
            raise ValueError("Invalid patient")

        if not callable(getattr(staff, "can_book_as_staff", None)) or not staff.can_book_as_staff():
            raise ValueError("Invalid staff")

        self.__patient = patient
        self.__staff = staff
        self.__status = Status.PENDING

    @property
    def id(self):
        return self.__id

    @property
    def patient(self):
        return self.__patient

    @property
    def staff(self):
        return self.__staff

    @property
    def start_hour(self):
        return self.__start_hour

    @property
    def status(self):
        return self.__status.value

    def is_active(self):
        return self.__status != Status.CANCELLED

    def confirm(self, clock):
        if self.__status != Status.PENDING:
            raise ValueError("Appointment is not pending")

        if clock.now() >= self.__start_hour:
            raise ValueError("Appointment has already started")

        self.__status = Status.CONFIRMED

    def cancel(self, clock):
        if self.__status == Status.CANCELLED:
            raise ValueError("Appointment already cancelled")

        if clock.now() >= self.__start_hour:
            raise ValueError("Appointment already started")

        if self.__status == Status.CONFIRMED and self.__start_hour - clock.now() < 2:
            raise ValueError("too late")

        self.__status = Status.CANCELLED


# Question 4: Logging

class AppointmentLog:
    def __init__(self, filename="appointments.log"):
        self.__filename = filename

    @contextmanager
    def open_log(self):
        with open(self.__filename, "a", encoding="utf-8") as file:
            print("[log] opened")
            try:
                yield file
            finally:
                print("[log] closed")


# Question 6: Clinic and buffer rules

# Clinic invariants:
# Person IDs are unique across registered people; appointment IDs are unique.
# Active appointments cannot overlap for the same patient or staff member.
# Staff appointments respect the staff object's bufferHours() value.
# Cancelled appointments do not block new bookings.

class Clinic:
    def __init__(self, clock, filename="appointments.log"):
        self.__clock = clock
        self.__people = {}
        self.__appointments = {}
        self.__log = AppointmentLog(filename)

    def add_person(self, person):
        with self.__log.open_log() as log:
            try:
                if person.id in self.__people:
                    raise ValueError("ID already exists")

                log.write(f"ADDED {person.role()} #{person.id}\n")
                self.__people[person.id] = person
                print("Added:", person.name)

            except Exception as error:
                log.write(f"FAILED add person: {error}\n")
                raise

    def appointments(self):
        return tuple(self.__appointments.values())

    def get_appointment(self, appointment_id):
        if appointment_id not in self.__appointments:
            raise ValueError("Appointment not found")
        return self.__appointments[appointment_id]

    def book(self, appointment_id, patient, staff, start_hour):
        with self.__log.open_log() as log:
            try:
                appointment_id = whole_number(appointment_id, 1)
                start_hour = whole_number(start_hour, 0, 167)

                if appointment_id in self.__appointments:
                    raise ValueError("Appointment ID already exists")

                if (self.__people.get(patient.id) is not patient
                        or not callable(getattr(patient, "can_book_as_patient", None))
                        or not patient.can_book_as_patient()):
                    raise ValueError("Patient not registered")

                if (self.__people.get(staff.id) is not staff
                        or not callable(getattr(staff, "can_book_as_staff", None))
                        or not staff.can_book_as_staff()):
                    raise ValueError("Staff not registered")

                if start_hour < self.__clock.now():
                    raise ValueError("Cannot book in the past")

                appointment = Appointment(
                    appointment_id, patient, staff, start_hour
                )

                for existing in self.__appointments.values():
                    if not existing.is_active():
                        continue

                    if existing.patient is patient:
                        if existing.start_hour == start_hour:
                            raise ValueError("Patient already booked")

                    if existing.staff is staff:
                        distance = abs(existing.start_hour - start_hour)

                        if distance < 1 + staff.bufferHours():
                            raise ValueError(
                                "Staff appointment or buffer conflict"
                            )

                log.write(f"BOOKED #{appointment_id}\n")
                self.__appointments[appointment_id] = appointment
                print("Booked appointment:", appointment_id)
                return appointment

            except Exception as error:
                log.write(f"FAILED book #{appointment_id}: {error}\n")
                raise

    def confirm(self, appointment_id):
        with self.__log.open_log() as log:
            try:
                appointment = self.get_appointment(appointment_id)
                appointment.confirm(self.__clock)

                log.write(f"CONFIRMED #{appointment_id}\n")
                print("Confirmed appointment:", appointment_id)

            except Exception as error:
                log.write(f"FAILED confirm #{appointment_id}: {error}\n")
                raise

    def cancel(self, appointment_id):
        with self.__log.open_log() as log:
            try:
                appointment = self.get_appointment(appointment_id)
                appointment.cancel(self.__clock)

                log.write(f"CANCELLED #{appointment_id}\n")
                print("Cancelled appointment:", appointment_id)

            except Exception as error:
                log.write(f"FAILED cancel #{appointment_id}: {error}\n")
                raise
