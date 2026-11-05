from clinic import (
    Clock, Person, Patient, Doctor, Nurse,
    Pharmacist, MedicalLecturer, Clinic
)


# Question 8: Main program demonstration
def main():
    print("CLINIC APPOINTMENT SYSTEM")
    print("P = 10")

    clock = Clock(0)
    clinic = Clinic(clock)

    # Question 1: Create patients and staff
    patient1 = Patient("Elias", 1)
    patient2 = Patient("Tariro", 2)
    patient3 = Patient("Simba", 3)

    doctor = Doctor("Dr Hove", 4)
    nurse = Nurse("Nurse Tshuma", 5)
    pharmacist = Pharmacist("Mr Moyo", 6)

    people = [
        patient1, patient2, patient3,
        doctor, nurse, pharmacist
    ]

    for person in people:
        clinic.add_person(person)

    # Question 3: Display staff fees using polymorphism
    print("\nSTAFF ROLES AND FEES")

    staff_members = [doctor, nurse, pharmacist]

    for staff in staff_members:
        print(staff.role(), "- Fee:", staff.fee())

    # Question 6: Book appointments
    print("\nBOOKING APPOINTMENTS")

    clinic.book(1, patient1, doctor, 10)
    clinic.book(2, patient2, nurse, 10)
    clinic.book(3, patient3, pharmacist, 11)

    # Question 2: Confirm an appointment
    print("\nCONFIRMING APPOINTMENT")

    clinic.confirm(1)

    # Question 6: Deliberate buffer conflict
    print("\nTESTING DOCTOR BUFFER")

    try:
        clinic.book(4, patient2, doctor, 11)
    except ValueError as error:
        print("Booking failed:", error)

    # Question 6: Valid booking after the buffer
    print("\nBOOKING AFTER BUFFER")

    clinic.book(5, patient2, doctor, 13)

    # Question 2: Cancel a pending appointment
    print("\nCANCELLING PENDING APPOINTMENT")

    clinic.cancel(3)

    # Question 2: Test late cancellation
    print("\nTESTING LATE CANCELLATION")

    clock.set_hour(9)

    try:
        clinic.cancel(1)
    except ValueError as error:
        print("Cancellation failed:", error)

    # Question 2: A cancelled appointment cannot return
    print("\nTESTING CANCELLED APPOINTMENT")

    try:
        clinic.confirm(3)
    except ValueError as error:
        print("Confirmation failed:", error)

    # Question 5: Multiple inheritance
    print("\nMEDICAL LECTURER")

    before = Person.constructor_count

    lecturer = MedicalLecturer(
        "Dr Shumba", 7, "Anatomy"
    )

    after = Person.constructor_count

    print("Name:", lecturer.name)
    print("Role:", lecturer.role())
    print("Module:", lecturer.module)
    print("Fee:", lecturer.fee())
    print("Person constructor calls:", after - before)

    # Question 2: Display appointment statuses
    print("\nAPPOINTMENT SUMMARY")

    for appointment in clinic.appointments():
        print(
            "Appointment:", appointment.id,
            "| Patient:", appointment.patient.name,
            "| Staff:", appointment.staff.name,
            "| Hour:", appointment.start_hour,
            "| Status:", appointment.status
        )

    print("\nDEMONSTRATION COMPLETED")


if __name__ == "__main__":
    main()
