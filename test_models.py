#     test classroom model
from models import classroom

classroomManager = classroom.ClassroomManager()

classroomManager.load_classrooms()

for classr in classroomManager.classroom:
    print(classr.lop, classr.teachers, type(classr.students))

print("Load dc rồi mom ơi!")

new_classroom = {
      "khoi" : 7,
      "lop" : "7A",
      "gvcn" : "L",
      "gvbm": {
         "khtn": "A",
         "anh": "D",
         "van": "C",
         "toan": "T"
      },
      "students" : ""
   }
classroomManager.add_classroom(new_classroom)

for classr in classroomManager.classroom:
    print(classr.lop, classr.teachers, type(classr.students))

print("THêm đuihưc rồi mẹ ơi")

lop = "7A"
classroomManager.remove_classroom(lop)

for classr in classroomManager.classroom:
    print(classr.lop, classr.teachers, type(classr.students))

print("Test load lop list")
print(classroomManager.get_lop_list())

print("Test get_available_teachers trong model claasroom")
teas = classroomManager.get_available_teachers()

print(teas)
   # test teacher model
# from models import teacher

# TeacherManager = teacher.TeacherManager()

# TeacherManager.load_teacher()

# for teacher in TeacherManager.teacher_data:
#     print(teacher.name, teacher.mon)

# print("Load dc rồi mom ơi!")

# new_teacher = {
#       "ten" : "Ly Suni",
#         "Joi tinh" : "Nu",
#         "Age" : 1,
#         "Mon Day" : "KHTN",
#         "GVCN Lop" : "6B"
#    }
# TeacherManager.add_teacher(new_teacher)

# for teacher in TeacherManager.teacher_data:
#     print(teacher.name, teacher.mon)

# print("THêm đuihưc rồi mẹ ơi")

# name = "Ly Suni"
# TeacherManager.remove_teacher(name)

# for teacher in TeacherManager.teacher_data:
#     print(teacher.name, teacher.mon)

# TEST OK HET ROI