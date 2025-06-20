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

lop = "9A"
classroomManager.remove_classroom(lop)

for classr in classroomManager.classroom:
    print(classr.lop, classr.teachers, type(classr.students))