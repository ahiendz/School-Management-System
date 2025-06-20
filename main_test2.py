from models import models

claasroommanager = models.ClassroomManager()

claasroommanager.load_classrooms()
for classroom in claasroommanager.classroom:
    print(f"Classroom Name: {classroom.name}, Teacher: {classroom.teacher}")
    for student in classroom.students:
        print(f"  Student: {student['name']}, ID: {student['id']}")

print()
classroom_dict = {
    "class": "6B",
    "teacher": "Mr. Hien",
    "students": []
}
claasroommanager.add_classroom(classroom_dict)
for classroom in claasroommanager.classroom:
    print(f"Classroom Name: {classroom.name}, Teacher: {classroom.teacher}")
    for student in classroom.students:
        print(f"  Student: {student['name']}, ID: {student['id']}")

print()
claasroommanager.remove_classroom("6A")
for classroom in claasroommanager.classroom:
    print(f"Classroom Name: {classroom.name}, Teacher: {classroom.teacher}")
    for student in classroom.students:
        print(f"  Student: {student['name']}, ID: {student['id']}")