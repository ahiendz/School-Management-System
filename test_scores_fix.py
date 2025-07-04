from models.student import Student

ob = Student(
    id="12345",
    name="John Doe",
    gender="Nam",
    dob="2000-01-01",
    parent_account="parent123",
    parent_password="password123",
    class_name="Class A",
    scores= {
            "Toán": {
                "semester_1": {
                    "oral_scores": [1, 2],
                    "quiz_15min": [2, 3],
                    "test_1period": [4, 5],
                    "midterm": 4,
                    "final": 10,
                    "average": None
                },
                "semester_2": {
                    "oral_scores": [],
                    "quiz_15min": [],
                    "test_1period": [],
                    "midterm": None,
                    "final": None,
                    "average": None
                }
            },
            "Văn": {
                "semester_1": {
                    "oral_scores": [],
                    "quiz_15min": [],
                    "test_1period": [],
                    "midterm": None,
                    "final": None,
                    "average": None
                },
                "semester_2": {
                    "oral_scores": [],
                    "quiz_15min": [],
                    "test_1period": [],
                    "midterm": None,
                    "final": None,
                    "average": None
                }
            },
            "KHTN": {
                "semester_1": {
                    "oral_scores": [],
                    "quiz_15min": [],
                    "test_1period": [],
                    "midterm": None,
                    "final": None,
                    "average": None
                },
                "semester_2": {
                    "oral_scores": [],
                    "quiz_15min": [],
                    "test_1period": [],
                    "midterm": None,
                    "final": None,
                    "average": None
                }
            },
            "Anh": {
                "semester_1": {
                    "oral_scores": [],
                    "quiz_15min": [],
                    "test_1period": [],
                    "midterm": None,
                    "final": None,
                    "average": None
                },
                "semester_2": {
                    "oral_scores": [],
                    "quiz_15min": [],
                    "test_1period": [],
                    "midterm": None,
                    "final": None,
                    "average": None
                }
            }
        },
    comment= None
)
average = ob.tinh_diem_trung_binh("Toán", "semester_1")
if average is not None:
    print(f"Điểm trung bình của {ob.name} trong môn Toán học kỳ 1 là: {average}")