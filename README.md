# CLINIC_APPOINTMENT_SYSTEM 
Elias S Hove R2420399 ,Tariro Tshuma R2420382

CLINIC APPOINTMENT SYSTEM
Programming Language: Python
P Value: 10

Question 1: Classes Used
This project is a clinic appointment system that allows patients to book appointments with medical staff. It also allows appointments to be confirmed and cancelled.

The following classes are used:

Person: The parent class that stores a person's name and ID.
Patient: Represents a patient who wants an appointment.
Staff: An abstract class for clinic employees.
Doctor: A staff member who charges 40.
Nurse: A staff member who charges 11.
Pharmacist: A staff member who charges 5.
Appointment: Stores appointment details such as patient, staff, starting hour and status.
Clinic: Manages patients, staff and appointments.
Clock: Provides the current hour.
Lecturer: Stores the module taught by a lecturer.
MedicalLecturer: Combines the Doctor and Lecturer classes.
The class diagram is shown below this README.

Question 2: Encapsulation and Appointment Status
I used private attributes to protect the information stored inside the classes.

In Python, attributes beginning with two underscores are name-mangled, which helps prevent accidental direct access.

When returning a list of appointments, the program returns a copy instead of the original list. This prevents another part of the program from changing the clinic's appointments directly.

An appointment can have three statuses:

PENDING
CONFIRMED
CANCELLED
The allowed changes are:

PENDING → CONFIRMED
PENDING → CANCELLED
CONFIRMED → CANCELLED

A cancelled appointment cannot become active again.

A confirmed appointment cannot be cancelled when less than 2 hours remain before its starting time.

An appointment cannot be cancelled after it has started.

Constructors reject empty names and IDs that are zero or negative by raising ValueError.

Question 3: Polymorphism and Fees
For this project, P = 10.

Doctor's fee:

40 + 5 × (10 % 5) = 40

Nurse's fee:

10 + (10 % 3) = 11

Pharmacist's fee:

5

Staff	Fee
Doctor	40
Nurse	11
Pharmacist	5
I used polymorphism so that each staff class provides its own fee() method.

The program calls role() and fee() in one loop without checking the staff member's type.

If another staff class is added, the same loop can still be used.

Question 4: Appointment Logging
The clinic records successful and failed actions in a log file.

I used Python's with statement to open and close the file.

The program displays:

[log] opened
[log] closed

The with statement closes the file even when an error occurs during the operation.

A failed action is also recorded. For example:

FAILED cancel #3: too late

If writing to the file fails, the program should report the logging error rather than pretending that the action was logged successfully.

Question 5: Multiple Inheritance
I created a Lecturer class with a module name.

The MedicalLecturer class inherits from Doctor and Lecturer.

Its role() method returns:

Doctor and Lecturer

I used super() and cooperative constructors so that Person is initialized only once.

A counter in the Person constructor is used to demonstrate this.

MedicalLecturer uses the Doctor fee, which is 40 for P = 10, because it is providing a medical service as a doctor.

In Java, Lecturer would be an interface because Java does not allow a class to extend two classes. MedicalLecturer would extend Doctor and implement Lecturer.

Question 6: Booking Rules and Buffer
The clinic checks that a patient or staff member does not have two active appointments at the same hour.

It also checks that IDs are unique within the clinic.

For this project:

10 % 4 = 2

Therefore, the assigned feature is Buffer.

The buffer requirements are:

Staff	Buffer
Doctor	2 hours
Nurse	1 hour
Pharmacist	0 hours
Every appointment lasts exactly one hour.

For example, if a doctor has an appointment starting at hour 10, the next appointment with that doctor can start at hour 13.

This leaves hours 11 and 12 free.

The Clinic calls bufferHours() on the staff object instead of checking whether the staff member is a doctor, nurse or pharmacist.

If a booking breaks a rule, the program rejects it and records the failed attempt.

Question 7: Design Decisions
D1. Where does the 2-hour cancellation rule belong?
I placed the rule in the Appointment class because it controls whether an appointment can change its status.

I also considered placing it in Clinic, but this would make Clinic responsible for more rules.

The advantage of keeping it in Appointment is that the rule stays close to the information it uses.

D2. Why is the clock testable?
The program gets the current hour from a Clock object instead of reading the computer's time.

This allows me to set a particular hour when testing.

For example, I can set the clock to hour 9 and test an appointment starting at hour 10.

If the program used the computer's actual time, testing exact cancellation deadlines would be harder.

D3. What changed when Pharmacist was added?
I added the Pharmacist class and gave it its own fee and buffer methods.

The Clinic and staff-printing loop did not need type checks.

The demonstration code was updated to create a pharmacist.

D4. What should MedicalLecturer.fee() return?
It should return 40 because it uses the Doctor fee.

Python's method resolution order and cooperative super() calls allow the shared Person constructor to run once.

Without proper constructor cooperation, Person might be initialized more than once, or one parent class might not be initialized correctly.

D5. What happens when logging fails?
If the log cannot be written or closed, the program should report the error.

It should not display a successful logging message when the file operation failed.

A failed log operation must not be silently ignored.

D6. Why use bufferHours() instead of checking types?
Each staff class knows how much time it needs between appointments.

Doctor returns 2, Nurse returns 1 and Pharmacist returns 0.

The Clinic simply calls bufferHours().

This makes the program easier to extend because a new staff class can provide its own buffer without changing the Clinic's booking logic.

Question 8: Program Demonstration
The main.py file demonstrates the following:

Creating patients and staff.
Printing staff roles and fees.
Booking appointments.
Confirming appointments.
Cancelling appointments.
Rejecting appointments that break booking rules.
Applying the staff buffer rules.
Recording successful and failed actions.
Demonstrating MedicalLecturer and the Person constructor counter.
The program also includes a deliberate failed booking to show that the rules are working.

For the unseen change request, the existing class structure allows new staff types or different buffer values to be added without rewriting the booking loop.

How to Run
Save clinic.py and main.py in the same folder.

Open a terminal in that folder and enter:

python main.py
The program will display the appointment operations and create an appointment log.
