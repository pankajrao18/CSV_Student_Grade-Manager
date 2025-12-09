import csv

class InvalidMarksError(Exception):
    pass


class Student:
    def __init__(self, student_id, name, m1, m2, m3):
        self.student_id = student_id
        self.name = name
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.total = 0
        self.percentage = 0
        self.grade = ""


class GradeCalculator:

    def check_mark(self, mark):
        if mark < 0 or mark > 100:
            raise InvalidMarksError("Marks must be between 0 and 100: " + str(mark))

    def calculate(self, student):
        self.check_mark(student.m1)
        self.check_mark(student.m2)
        self.check_mark(student.m3)

        student.total = student.m1 + student.m2 + student.m3
        student.percentage = student.total / 3

        if student.percentage >= 90:
            student.grade = "A+"
        elif student.percentage >= 80:
            student.grade = "A"
        elif student.percentage >= 70:
            student.grade = "B"
        elif student.percentage >= 60:
            student.grade = "C"
        elif student.percentage >= 50:
            student.grade = "D"
        else:
            student.grade = "F"


def read_students(file_name):
    students = []

    try:
        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            first_row = True

            for row in reader:
                if first_row:
                    first_row = False
                    continue

                if len(row) < 5:
                    print("Skipped row (not enough columns):", row)
                    continue

                try:
                    s = Student(
                        row[0].strip(),
                        row[1].strip(),
                        float(row[2]),
                        float(row[3]),
                        float(row[4])
                    )
                    students.append(s)

                except ValueError:
                    print("Skipped row (invalid number):", row)

    except FileNotFoundError:
        print("Input file not found:", file_name)

    return students


def write_students(file_name, students, append = False):
    mode = "a" if append else "w"

    with open(file_name, mode, newline="") as file:
        writer = csv.writer(file)

        if not append:
            writer.writerow([
                "ID", "Name", "Mark1", "Mark2", "Mark3",
                "Total", "Percentage", "Grade"
            ])

        for s in students:
            writer.writerow([
                s.student_id,
                s.name,
                s.m1,
                s.m2,
                s.m3,
                round(s.total, 2),
                round(s.percentage, 2),
                s.grade
            ])


def main():
    input_file = "students.csv"
    output_file = "student_grades.csv"

    calc = GradeCalculator()

    print("Reading student records from:", input_file)
    students = read_students(input_file)

    valid_students = []

    for s in students:
        try:
            calc.calculate(s)
            valid_students.append(s)
        except InvalidMarksError as e:
            print("Error for Student", s.student_id, "-", s.name + ":", e)

    if valid_students:
        write_students(output_file, valid_students, append=False)
        print("Results saved to:", output_file)
    else:
        print("No valid students to save.")

    add_more = input("Do you want to add a new student manually? (yes/no): ").lower()

    if add_more == "y":
        try:
            sid = input("Enter Student ID: ")
            name = input("Enter Name: ")
            m1 = float(input("Enter Mark1: "))
            m2 = float(input("Enter Mark2: "))
            m3 = float(input("Enter Mark3: "))

            new_student = Student(sid, name, m1, m2, m3)
            calc.calculate(new_student)

            write_students(output_file, [new_student], append=True)
            print("New student record added successfully.")

        except ValueError:
            print("Invalid input. Marks must be numbers.")

        except InvalidMarksError as e:
            print("Cannot add student:", e)


if __name__ == "__main__":
    main()
