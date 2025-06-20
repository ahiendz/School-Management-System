# Run here to start the application
from views import login_side as login
import sys

if __name__ == "__main__":
    app = login.QApplication(sys.argv)
    main_window = login.login()
    sys.exit(app.exec())