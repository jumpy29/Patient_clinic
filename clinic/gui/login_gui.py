from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon

class LoginDashBoard(QWidget):
    #emits a login signal
    login_button_clicked_signal = pyqtSignal(str, str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOGIN")
        self.layout = QVBoxLayout()

        #input fields
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        
        self.username_input.setFixedSize(QSize(200, 40))
        self.password_input.setFixedSize(QSize(200, 40))

        #adding placeholder
        self.username_input.setPlaceholderText("Username")  
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEnabled(False) #allowing only when username entered
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hiding password input

        #sending signals when info entered
        self.username_input.textChanged.connect(self.username_entered)
        self.password_input.textChanged.connect(self.password_entered)

        #login button
        self.login_button = QPushButton("Login")
        self.login_button.setFixedSize(QSize(150, 30))
        self.login_button.setEnabled(False) #initially button disabled
        self.login_button.clicked.connect(self.login_button_clicked) #connecting button

        #adding them to layout and aligning
        self.layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(self.layout)

    def login_button_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        #sending signal to main window with username and password
        self.login_button_clicked_signal.emit(username, password)

    #enabling password entry
    def username_entered(self):
        self.password_input.setEnabled(True)
    
    #enabling login button
    def password_entered(self):
        self.login_button.setEnabled(True)

    #clearing password and username
    def refresh(self):
        self.username_input.setText("")
        self.password_input.setText("")
        self.password_input.setEnabled(False)
        self.login_button.setEnabled(False)