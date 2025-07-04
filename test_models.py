#     test classroom model
from models import classroom

classroomManager = classroom.ClassroomManager()

classroomManager.load_classrooms()

for classr in classroomManager.classroom:
    print(classr.lop, classr.teachers)

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
      }
   }
classroomManager.add_classroom(new_classroom)

for classr in classroomManager.classroom:
    print(classr.lop, classr.teachers)

print("THêm đuihưc rồi mẹ ơi")

lop = "7A"
classroomManager.remove_classroom(lop)

for classr in classroomManager.classroom:
    print(classr.lop, classr.teachers)

print("Test load lop list")
print(classroomManager.get_lop_list())

print("Test get_available_classroom")
available_classes = classroomManager.get_available_classroom()
print(available_classes)

# TEST OK HET ROI