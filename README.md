# CLINIC APPOINTMENT SYSTEM

**Group Members:**

Elias S Hove — R2420399  
Tariro Tshuma — R2420382

Programming Language: Python  
Value of P: 10




## Question 1: Classes Used

Our project is a clinic appointment system that allows patients to book appointments with medical staff. Appointments can also be confirmed or cancelled.

We created the following classes:

1. **Person:** An abstract class that stores a person's name and ID and defines the abstract `role()` method.
2. **Patient:** Inherits from Person and represents a patient booking an appointment.
3. **Staff:** An abstract class that inherits from Person and defines the abstract `fee()` method.
4. **Doctor:** Inherits from Staff and represents a doctor.
5. **Nurse:** Inherits from Staff and represents a nurse.
6. **Pharmacist:** Inherits from Staff and represents a pharmacist.
7. **Appointment:** Stores the appointment ID, patient, staff member, starting hour and status.
8. **Clinic:** Manages registered people and appointments.

### Class Diagram

                                    Person (abstract)
                         - name
                         - id
                         + role() [abstract]
                                |
                  +-------------+-------------+
                  |                           |
               Patient                  Staff (abstract)
               + role()                 + fee() [abstract]
                                        + bufferHours() [abstract]
                                               |
                              +----------------+----------------+
                              |                |                |
                           Doctor            Nurse          Pharmacist
                           + role()          + role()        + role()
                           + fee()           + fee()         + fee()
                           + bufferHours()   + bufferHours() + bufferHours()


    Clinic --------------------> Appointment
      |                            |
      |                            +----------> Patient
      |                            |
      |                            +----------> Staff
      |
      +---- uses --------------> Clock
      |
      +---- uses --------------> AppointmentLog


    Appointment ----------------> Status
                                  PENDING
                                  CONFIRMED
                                  CANCELLED


    Doctor --------------------> MedicalLecturer
                                     |
                                     +----------> Lecturer
                                                  - module
                                                  + role()







## Question 2: Encapsulation and Appointment Status

We used private attributes to protect information stored in the classes.

In Python, attributes beginning with two underscores are name-mangled, which helps prevent accidental direct access.

The Clinic returns a tuple of appointments instead of its internal dictionary. This prevents other parts of the program from directly changing the appointment collection.

Appointments have three possible statuses:

- PENDING
- CONFIRMED
- CANCELLED

The legal status changes are:

PENDING → CONFIRMED  
PENDING → CANCELLED  
CONFIRMED → CANCELLED

A cancelled appointment cannot become active again.

A confirmed appointment cannot be cancelled less than two hours before its starting time. No appointment can be cancelled once it has started.

Constructors reject empty names and IDs that are zero or negative by raising `ValueError`.

The invariants of Appointment and Clinic are written as comments above the classes in the source code.







## Question 3: Polymorphism and Fees

For our project, P = 10.

Doctor's fee:

40 + 5 × (10 % 5) = 40

Nurse's fee:

10 + (10 % 3) = 11

Pharmacist's fee:

5

| Staff | Fee |
|---|---|
| Doctor | 40 |
| Nurse | 11 |
| Pharmacist | 5 |

We used polymorphism by giving each staff class its own `fee()` and `role()` methods.

The program uses one loop to display the role and fee of each staff member without checking the staff member's type.

This means another Staff subclass can be added without changing the loop or Clinic.







## Question 4: Appointment Logging

The Clinic records successful and failed actions in an appointment log.

We used Python's `with` statement to open and close the log file.

When the log is used, the program displays:

```text
[log] opened
[log] closed
```

The `with` statement makes sure the file is closed even if an error occurs during the operation.

Failed operations are also recorded. For example:

```text
FAILED cancel #3: too late
```

This helps us identify which operations were successful and which ones failed.







## Question 5: Multiple Inheritance

We created a Lecturer class that stores a module name.

MedicalLecturer inherits from both Doctor and Lecturer.

Its `role()` method returns:

```text
Doctor and Lecturer
```

We used `super()` and cooperative constructors so that Person is initialized only once.

A counter in the Person constructor is used to demonstrate this.

MedicalLecturer returns a fee of 40 because it provides the same medical service as Doctor.

In Java, Lecturer would be an interface because Java does not allow a class to extend two classes. MedicalLecturer would extend Doctor and implement Lecturer.






## Question 6: Booking Rules and Buffer

The Clinic checks that a patient or staff member does not have two active appointments at the same hour.

It also checks that IDs are unique.

For this project:

10 % 4 = 2

Therefore, our assigned feature is **Buffer**.

| Staff     |     Buffer |
|-----------|------------|
| Doctor    | 2 hours    |
| Nurse     | 1 hour     |
| Pharmacist| 0 hours    |

Every appointment lasts exactly one hour.

For example, if a doctor has an appointment starting at hour 10, another appointment with the same doctor can start at hour 13.

This leaves hours 11 and 12 free.

The Clinic gets the required gap by calling `bufferHours()` on the staff object instead of checking the staff member's type.

If a booking breaks any rule, it is rejected and the failed attempt is recorded in the log.






## Question 7: Design Decision Log

### D1. Where does the 2-hour cancellation rule belong?

We placed the rule in the Appointment class because Appointment controls its own status.

We also considered placing it in Clinic, but this would give Clinic more responsibilities.

Keeping the rule in Appointment makes the code easier to understand and maintain.

### D2. Why is the clock design testable?

We created a Clock class that stores the current hour.

The program calls `Clock.now()` instead of reading the computer's actual time.

This allows us to set different hours during testing.

For example, we can set the clock to hour 9 and test whether an appointment starting at hour 10 can be cancelled.

Using the actual computer time would make it difficult to test specific cancellation deadlines.

### D3. What changed when Pharmacist was added?

We added the Pharmacist class and implemented its `role()`, `fee()` and `bufferHours()` methods.

We also added a pharmacist object to the demonstration.

The Clinic and staff-printing loop did not need to be changed because they use polymorphism.

### D4. What should MedicalLecturer.fee() return?

MedicalLecturer returns 40 because it inherits the Doctor fee.

Python's method resolution order and cooperative `super()` calls allow Person to be initialized once.

Without proper constructor cooperation, Person could be initialized twice or one of the parent classes might not be initialized correctly.

### D5. What happens when logging fails?

If writing to or closing the log fails, the program should report the error.

It should not silently ignore the failure or claim that logging was successful.

This is important because the log is used to keep records of clinic operations.

### D6. Why use bufferHours() instead of checking types?

We used `bufferHours()` because each staff class knows how much time it needs between appointments.

Doctor returns 2, Nurse returns 1 and Pharmacist returns 0.

Clinic calls the same method for every staff member.

This makes it easier to add another staff class without changing the Clinic's booking rules.








## Question 8: Program Demonstration

Our `main.py` demonstrates the following:

1. Creating patients and staff.
2. Displaying staff roles and fees.
3. Booking appointments.
4. Confirming appointments.
5. Cancelling appointments.
6. Rejecting bookings that break the rules.
7. Applying the buffer rules.
8. Recording successful and failed operations.
9. Demonstrating MedicalLecturer and the Person constructor counter.

We also included deliberate failures to show that the appointment rules are working.

The program is designed so that new staff classes can be added without changing the existing booking logic.

---

<!-- ## Running the Program

The project contains the following files:

```text
Clinic_Appointment_System/
    clinic.py
    main.py
    README.md
```

To run the program, open the project folder in VS Code and enter:

```bash
python main.py
```

The program displays the appointment operations and creates an `appointments.log` file. -->