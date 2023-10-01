# Import necessary PyQt6 modules
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox, QDateEdit
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
import mysql.connector
from PyQt6.uic.properties import QtCore

# Define a class for managing database connections
class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="p@ssw0rd_2023", database="registration"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    # Method to establish a connection to the database
    def connect(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                             database=self.database)
        return connection

# Define a global variable for storing the selected student ID
selected_student_id = None

# Define the main application window as a subclass of QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maasin Day Care Center Registration System")
        self.setMinimumSize(800, 600)

        # Create menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        search_menu_item = self.menuBar().addMenu("&Search")

        # Create actions for menu items
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        search_menu_item.addAction(search_action)

        # Create a toolbar and add elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add a search box (QLineEdit) to the toolbar
        self.search_input = QLineEdit()
        toolbar.addWidget(self.search_input)

        # Add a search button (QPushButton) to the toolbar
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        toolbar.addWidget(search_button)

        # Create a table widget and set it as the central widget
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels((
            "Student ID", "Firstname", "Lastname", "Middlename", "Birthdate", "Gender",
            "Address", "Guardian", "Mobile Number"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create a status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Load data into the table
        self.load_data()

        # Detect a cell click and connect it to a method
        self.table.cellClicked.connect(self.cell_clicked)
        self.table.clicked.connect(self.select_record)

    # Method to select a record in the table
    def select_record(self):
        global selected_student_id  # Use the global variable

        # Get the currently selected row
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            # Retrieve data from the selected row
            record_id = self.table.item(selected_row, 0).text()
            self.firstname = self.table.item(selected_row, 1).text()
            self.lastname = self.table.item(selected_row, 2).text()
            self.middlename = self.table.item(selected_row, 3).text()
            self.birthdate = self.table.item(selected_row, 4).text()
            self.gender = self.table.item(selected_row, 5).text()
            self.address = self.table.item(selected_row, 6).text()
            self.guardian = self.table.item(selected_row, 7).text()
            self.mobile_number = self.table.item(selected_row, 8).text()

            # Set the global variable to the selected record_id
            selected_student_id = record_id

    # Method to handle cell clicks in the table
    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        record_button = QPushButton("Check Record")
        record_button.clicked.connect(self.record)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
        self.statusbar.addWidget(record_button)

    # Method to load data from the database into the table
    def load_data(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM student_info")
            result = cursor.fetchall()
            self.table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            connection.close()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Loading of student record failed!')
            print(f"An error occurred: {e}")

    # Method to open the insert dialog
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    # Method to perform a search based on the input in the search box
    def search(self):
        try:
            name = self.search_input.text()
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM student_info WHERE firstname = %s", (name,))
            result = cursor.fetchall()
            cursor.close()
            connection.close()

            # Clear the table
            self.table.setRowCount(0)

            # Populate the table with search results
            for row in result:
                self.table.insertRow(self.table.rowCount())
                for col, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(self.table.rowCount() - 1, col, item)
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Searching of student record failed!')
            print(f"An error occurred: {e}")

    # Method to open the edit dialog
    def edit(self):
        edit_dialog = EditDialog(self.firstname, self.lastname, self.middlename, self.birthdate, self.gender,
                                 self.address, self.guardian, self.mobile_number)
        edit_dialog.exec()

    # Method to open the delete dialog
    def delete(self):
        delete_dialog = DeleteDialog()
        delete_dialog.exec()

    # Method to open the about dialog
    def about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

    # Method to open the record dialog
    def record(self):
        record_dialog = CheckRecord()
        record_dialog.exec()

# Define the AboutDialog as a subclass of QMessageBox
class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created for learning purposes
        """
        self.setText(content)

# Define the EditDialog as a subclass of QDialog
class EditDialog(QDialog):
    def __init__(self, firstname, lastname, middlename, birthdate, gender, address, guardian, mobile_number):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
        self.birthdate = birthdate
        self.gender = gender
        self.address = address
        self.guardian = guardian
        self.mobile_number = mobile_number

        layout = QVBoxLayout()

        # Add student firstname widget
        self.student_firstname = QLineEdit(self.firstname)
        self.student_firstname.setPlaceholderText("Firstname")
        layout.addWidget(self.student_firstname)

        # Add student lastname widget
        self.student_lastname = QLineEdit(self.lastname)
        self.student_lastname.setPlaceholderText("Lastname")
        layout.addWidget(self.student_lastname)

        # Add student middlename widget
        self.student_middlename = QLineEdit(self.middlename)
        self.student_middlename.setPlaceholderText("Middlename")
        layout.addWidget(self.student_middlename)

        # Create a QLabel to serve as a textPlaceholder
        placeholder_label = QLabel("Birthdate (YYYY-DD-MM):")
        placeholder_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(placeholder_label)

        # Insert student birthday widget
        date_format = "yyyy-dd-MM"
        student_birthdate = QDate.fromString(self.birthdate, date_format)
        self.student_birthdate = QDateEdit(student_birthdate)
        self.student_birthdate.setCalendarPopup(True)  # Enable the calendar popup
        self.student_birthdate.setDisplayFormat("yyyy-dd-MM")
        layout.addWidget(self.student_birthdate)

        # Create a QLabel to serve as a textPlaceholder
        placeholder_label = QLabel("Gender:")
        placeholder_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(placeholder_label)

        # Add student gender widget
        self.student_gender = QComboBox()
        courses = ["Male", "Female"]
        self.student_gender.addItems(courses)
        self.student_gender.setCurrentText(self.gender)
        layout.addWidget(self.student_gender)

        # Add student address widget
        self.student_address = QLineEdit(self.address)
        self.student_address.setPlaceholderText("Address")
        layout.addWidget(self.student_address)

        # Add student guardian widget
        self.student_guardian = QLineEdit(self.guardian)
        self.student_guardian.setPlaceholderText("Guardian")
        layout.addWidget(self.student_guardian)

        # Add mobile widget
        self.student_mobile = QLineEdit(self.mobile_number)
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)

        # Add a submit button
        self.button = QPushButton("Update")
        self.button.clicked.connect(self.update_student)
        layout.addWidget(self.button)

        self.setLayout(layout)

    # Method to update student data
    def update_student(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            global selected_student_id

            sql = "UPDATE student_info SET firstname = %s, lastname = %s, middlename = %s, birthdate = %s, gender = %s," \
                  "address = %s, guardian = %s, mobileno = %s" \
                  "WHERE pk_studentid = %s"
            cursor.execute(sql,
                           (self.student_firstname.text(), self.student_lastname.text(), self.student_middlename.text(),
                            self.student_birthdate.date().toString("yyyy-MM-dd"),
                            self.student_gender.itemText(self.student_gender.currentIndex()),
                            self.student_address.text(), self.student_guardian.text(), self.student_mobile.text(),
                            selected_student_id))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, 'Success', 'Data updated successfully!')
            main_window.load_data()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Data edit failed!')
            print(f"An error occurred: {e}")

# Define the DeleteDialog as a subclass of QDialog
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 1)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_button)

    # Method to delete a student record
    def delete_button(self):
        try:
            # Get select row index and student_id
            index = main_window.table.currentRow()
            student_id = main_window.table.item(index, 0).text()

            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            queries = ["DELETE from record_info WHERE fk_studentid = %s",
                       "DELETE from student_info WHERE pk_studentid = %s"]
            for query in queries:
                cursor.execute(query, (student_id,))
            connection.commit()
            cursor.close()
            connection.close()
            main_window.load_data()

            self.close()

            confirmation_widget = QMessageBox()
            confirmation_widget.setWindowTitle("Success")
            confirmation_widget.setText("The record was deleted successfully!")
            confirmation_widget.exec()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Delete student record failed!')
            print(f"An error occurred: {e}")

# Define the InsertDialog as a subclass of QDialog
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(295)

        layout = QVBoxLayout()

        # Add student firstname widget
        self.student_firstname = QLineEdit()
        self.student_firstname.setPlaceholderText("Firstname")
        layout.addWidget(self.student_firstname)

        # Add student lastname widget
        self.student_lastname = QLineEdit()
        self.student_lastname.setPlaceholderText("Lastname")
        layout.addWidget(self.student_lastname)

        # Add student middlename widget
        self.student_middlename = QLineEdit()
        self.student_middlename.setPlaceholderText("Middlename")
        layout.addWidget(self.student_middlename)

        # Create a QLabel to serve as a textPlaceholder
        placeholder_label = QLabel("Birthdate (YYYY-DD-MM):")
        placeholder_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(placeholder_label)

        # Insert student birthday widget
        self.student_birthdate = QDateEdit()
        self.student_birthdate.setCalendarPopup(True)  # Enable the calendar popup
        self.student_birthdate.setDisplayFormat("yyyy-dd-MM")
        layout.addWidget(self.student_birthdate)

        # Create a QLabel to serve as a textPlaceholder
        placeholder_label = QLabel("Gender:")
        placeholder_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(placeholder_label)

        # Add student gender widget
        self.student_gender = QComboBox()
        courses = ["Male", "Female"]
        self.student_gender.addItems(courses)
        layout.addWidget(self.student_gender)

        # Add student address widget
        self.student_address = QLineEdit()
        self.student_address.setPlaceholderText("Address")
        layout.addWidget(self.student_address)

        # Add student guardian widget
        self.student_guardian = QLineEdit()
        self.student_guardian.setPlaceholderText("Guardian")
        layout.addWidget(self.student_guardian)

        # Add mobile widget
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)

        # Create a submit button
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.add_student)
        layout.addWidget(self.button)

        self.setLayout(layout)

    # Method to add a new student record
    def add_student(self):
        try:
            firstname = self.student_firstname.text()
            lastname = self.student_lastname.text()
            middlename = self.student_middlename.text()
            birthdate = self.student_birthdate.date().toString("yyyy-MM-dd")
            gender = self.student_gender.currentText()
            address = self.student_address.text()
            guardian = self.student_guardian.text()
            mobile = self.student_mobile.text()

            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            sql = "INSERT INTO student_info " \
                  "(firstname, lastname, middlename, birthdate, gender, address, guardian, mobileno) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (firstname, lastname, middlename, birthdate, gender, address, guardian, mobile))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, 'Success', 'Data inserted successfully!')
            main_window.load_data()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Data insertion failed!')
            print(f"An error occurred: {e}")

# Define the CheckRecord class as a subclass of QDialog
class CheckRecord(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Record")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        layout = QVBoxLayout()

        self.teacher = None
        self.time_schedule = None
        self.attended_year = None

        self.enroll_button = QPushButton("Enroll")
        self.enroll_button.clicked.connect(self.enroll)
        self.enroll_button.setFixedSize(100, 40)  # Set the size of the button
        layout.addWidget(self.enroll_button)

        # Create a QTableWidget with 3 columns
        self.record_table = QTableWidget()
        self.record_table.setColumnCount(5)
        self.record_table.setHorizontalHeaderLabels(
            ["Record ID", "Assigned Teacher", "Time Schedule", "School Year", "Status"])

        # Add widgets to the layout
        layout.addWidget(self.record_table)

        # Set the layout for the dialog
        self.setLayout(layout)

        self.statusbar = QStatusBar()
        layout.addWidget(self.statusbar)

        self.load_record()
        self.record_table.clicked.connect(self.select_record)
        self.record_table.cellClicked.connect(self.cell_clicked)

    # Method to load the student records
    def load_record(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            global selected_student_id

            sql = "SELECT pk_recordid, teacher, timesched, schoolyear, status FROM record_info WHERE fk_studentid = %s"
            cursor.execute(sql, (selected_student_id,))
            result = cursor.fetchall()
            self.record_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.record_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.record_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            connection.close()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'loading of records failed!')
            print(f"An error occurred: {e}")

    # Method to select a record from the table
    def select_record(self):
        # Get the currently selected row
        selected_row = self.record_table.currentRow()

        if selected_row >= 0:
            # Retrieve data from the selected row
            self.record_id = self.record_table.item(selected_row, 0).text()
            self.teacher = self.record_table.item(selected_row, 1).text()
            self.time_schedule = self.record_table.item(selected_row, 2).text()
            self.attended_year = self.record_table.item(selected_row, 3).text()

    # Method to handle cell click events
    def cell_clicked(self):
        edit_button = QPushButton("Update Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    # Method to open the edit record dialog
    def edit(self):
        edit_dialog = UpdateRecordDialog(self.record_id, self.teacher, self.time_schedule, self.attended_year)
        edit_dialog.exec()

    # Method to open the delete record dialog
    def delete(self):
        delete_dialog = DeleteRecordDialog(self.record_id)
        delete_dialog.exec()

    # Method to open the enroll student dialog
    def enroll(self):
        enroll_dialog = EnrollStudentDialog()
        enroll_dialog.exec()

# Define the UpdateRecordDialog class as a subclass of QDialog
class UpdateRecordDialog(QDialog):
    def __init__(self, record_id, teacher, time_schedule, school_year):
        super().__init__()
        self.setWindowTitle("Update Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        self.record_id = record_id
        self.assigned_teacher = teacher
        self.assigned_schedule = time_schedule
        self.enrolled_year = school_year

        teacher_label = QLabel("Teacher Assigned:")
        teacher_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(teacher_label)

        self.teacher = QComboBox()
        teachers = ["Teacher 1", "Teacher 2"]
        self.teacher.addItems(teachers)
        self.teacher.setCurrentText(self.assigned_teacher)
        layout.addWidget(self.teacher)

        schedule_label = QLabel("Time Schedule:")
        schedule_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(schedule_label)

        self.time_schedule = QComboBox()
        schedule = ["8:00 AM - 10:00 AM", "10:30 AM - 12:30 PM", "1:00 PM - 3:00 PM"]
        self.time_schedule.addItems(schedule)
        self.time_schedule.setCurrentText(self.assigned_schedule)
        layout.addWidget(self.time_schedule)

        school_year_label = QLabel("School Year:")
        school_year_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(school_year_label)

        self.school_year = QLineEdit(self.enrolled_year)
        self.school_year.setPlaceholderText("YYYY-YYYY")
        layout.addWidget(self.school_year)

        # Add an update button
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_record)
        layout.addWidget(update_button)

        self.setLayout(layout)

    # Method to update the student record
    def update_record(self):
        try:
            assigned_teacher = self.teacher.currentText()
            assigned_schedule = self.time_schedule.currentText()
            enrolled_year = self.school_year.text()

            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            sql = "UPDATE record_info SET teacher = %s, timesched = %s, schoolyear = %s WHERE pk_recordid = %s"
            cursor.execute(sql, (assigned_teacher, assigned_schedule, enrolled_year, self.record_id))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, 'Success', 'Record updated successfully!')
            record_dialog.load_record()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Record update failed!')
            print(f"An error occurred: {e}")

# Define the DeleteRecordDialog class as a subclass of QDialog
class DeleteRecordDialog(QDialog):
    def __init__(self, record_id):
        super().__init__()
        self.setWindowTitle("Delete Student Record")

        self.record_id = record_id

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete this record?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 1)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_record)

    # Method to delete the student record
    def delete_record(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            sql = "DELETE FROM record_info WHERE pk_recordid = %s"
            cursor.execute(sql, (self.record_id,))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, 'Success', 'Record deleted successfully!')
            record_dialog.load_record()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Record delete failed!')
            print(f"An error occurred: {e}")

# Define the EnrollStudentDialog class as a subclass of QDialog
class EnrollStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enroll Student")
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        teacher_label = QLabel("Teacher Assigned:")
        teacher_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(teacher_label)

        self.teacher = QComboBox()
        teachers = ["Teacher 1", "Teacher 2"]
        self.teacher.addItems(teachers)
        layout.addWidget(self.teacher)

        schedule_label = QLabel("Time Schedule:")
        schedule_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(schedule_label)

        self.time_schedule = QComboBox()
        schedule = ["8:00 AM - 10:00 AM", "10:30 AM - 12:30 PM", "1:00 PM - 3:00 PM"]
        self.time_schedule.addItems(schedule)
        layout.addWidget(self.time_schedule)

        school_year_label = QLabel("School Year:")
        school_year_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(school_year_label)

        self.school_year = QLineEdit()
        self.school_year.setPlaceholderText("YYYY-YYYY")
        layout.addWidget(self.school_year)

        # Add an enroll button
        enroll_button = QPushButton("Enroll")
        enroll_button.clicked.connect(self.enroll_student)
        layout.addWidget(enroll_button)

        self.setLayout(layout)

    # Method to enroll the student
    def enroll_student(self):
        try:
            student_id = selected_student_id
            teacher = self.teacher.currentText()
            time_schedule = self.time_schedule.currentText()
            school_year = self.school_year.text()

            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            sql = "INSERT INTO record_info (fk_studentid, teacher, timesched, schoolyear, status) " \
                  "VALUES (%s, %s, %s, %s, 'Enrolled')"
            cursor.execute(sql, (student_id, teacher, time_schedule, school_year))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, 'Success', 'Student enrolled successfully!')
            record_dialog.load_record()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Student enrollment failed!')
            print(f"An error occurred: {e}")

# Create the main application instance
app = QApplication(sys.argv)

# Create the main window instance
main_window = MainWindow()

# Create the record dialog instance
record_dialog = CheckRecord()

# Show the main window
main_window.show()

# Run the application
sys.exit(app.exec())
