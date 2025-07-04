graph TD;
    subgraph "View (Giao diện)"
        AdminView["Admin Window"]
        TeacherView["Teacher Window"]
    end

    subgraph "Service Layer (Tầng Điều phối)"
        style ServiceLayer fill:#e6f3ff,stroke:#99c2ff
        ClassroomService["ClassroomService"]
        TeacherService["TeacherService"]
        StudentService["StudentService"]
        AuthService["AuthService (Đăng nhập)"]
    end

    subgraph "Model Layer (Tầng Dữ liệu)"
        style ModelLayer fill:#e6ffed,stroke:#99ffb3
        ClassroomManager["ClassroomManager"]
        TeacherManager["TeacherManager"]
        StudentManager["StudentManager"]
    end
    
    AdminView -- "Yêu cầu nghiệp vụ" --> ClassroomService
    AdminView -- "Yêu cầu nghiệp vụ" --> TeacherService
    AdminView -- "Yêu cầu nghiệp vụ" --> StudentService
    TeacherView -- "Yêu cầu nghiệp vụ" --> StudentService

    ClassroomService -- "Nói chuyện với" --> TeacherManager
    ClassroomService -- "Nói chuyện với" --> ClassroomManager
    
    TeacherService -- "Nói chuyện với" --> ClassroomManager
    TeacherService -- "Nói chuyện với" --> TeacherManager

    StudentService -- "Nói chuyện với" --> StudentManager
    StudentService -- "Nói chuyện với" --> ClassroomManager

    AuthService -- "Xác thực" --> TeacherManager
    AuthService -- "Xác thực" --> StudentManager
    
    View -- "Đăng nhập" --> AuthService

    linkStyle 7 stroke-dasharray: 5 5;
    linkStyle 8 stroke-dasharray: 5 5;
    linkStyle 9 stroke-dasharray: 5 5;
    linkStyle 10 stroke-dasharray: 5 5;
    linkStyle 11 stroke-dasharray: 5 5;
    linkStyle 12 stroke-dasharray: 5 5;
    linkStyle 13 stroke-dasharray: 5 5;
    
    
    ClassroomManager -.- TeacherManager
    ClassroomManager -.- StudentManager
    TeacherManager -.- StudentManager
    
    subgraph "Chú thích"
    NoLink["<b>KHÔNG</b><br>nói chuyện<br>trực tiếp<br>với nhau"]
    end
    
    ClassroomManager -- " " --- NoLink
    NoLink -- " " --- TeacherManager
    
    style NoLink fill:#ffcccc,stroke:red,stroke-width:2px,stroke-dasharray: 5 5