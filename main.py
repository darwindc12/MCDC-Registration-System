from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox, QDateEdit
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
import mysql.connector
from PyQt6.uic.properties import QtCore


class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="p@ssw0rd_2023", database="registration"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                             database=self.database)
        return connection

selected_record_id = None
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maasin Day Care Center Registration System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        search_menu_item = self.menuBar().addMenu("&Search")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        # add_action = QAction("Add", self)
        # help_menu_item.addAction(add_action)
        # add_action.triggered.connect(self.insert())

        search_action = QAction(QIcon("icons/icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        search_menu_item.addAction(search_action)

        # Create a toolbar and add toolbar elements
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

        # Set selection behavior to select entire rows

        # Create a table widget and set it as the central widget
        self.table = QTableWidget()

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels((
            "Student ID", "Firstname", "Lastname", "Middlename", "Birthdate", "Gender",
            "Address", "Guardian", "Mobile Number"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create a status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)
        self.table.clicked.connect(self.select_record)

    def select_record(self):
        global selected_record_id  # Use the global variable

        # Get the currently selected row
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            # Retrieve data from the selected row
            record_id = self.table.item(selected_row, 0).text()

            # Set the global variable to the selected record_id
            selected_record_id = record_id


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

    def load_data(self):
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

        return result



    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        name = self.search_input.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student_info WHERE firstname = %s", (name,))
        result = cursor.fetchall()
        cursor.close()
        connection.close()

        # Assuming 'table' is your Qt table widget
        student_management_sys.table.setRowCount(0)  # Clear the table
        for row in result:
            student_management_sys.table.insertRow(student_management_sys.table.rowCount())
            for col, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                student_management_sys.table.setItem(student_management_sys.table.rowCount() - 1, col, item)

    # def search(self):
    #     search_dialog = SearchDialog()
    #     search_dialog.exec()

    def edit(self):
        edit_dialog = EditDialog()
        edit_dialog.exec()

    def delete(self):
        delete_dialog = DeleteDialog()
        delete_dialog.exec()

    def about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

    def record(self):
        record_dialog = CheckRecord()
        record_dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created for learning purposes
        """
        self.setText(content)

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get student name from selected row
        index = student_management_sys.table.currentRow()
        student_firstname = student_management_sys.table.item(index, 1).text()
        self.student_id = student_management_sys.table.item(index, 0).text()

        # Add student firstname widget
        self.student_firstname = QLineEdit(student_firstname)
        self.student_firstname.setPlaceholderText("Firstname")
        layout.addWidget(self.student_firstname)

        # Add student lastname widget
        student_lastname = student_management_sys.table.item(index, 2).text()
        self.student_lastname = QLineEdit(student_lastname)
        self.student_lastname.setPlaceholderText("Lastname")
        layout.addWidget(self.student_lastname)

        # Add student middlename widget
        student_middlename = student_management_sys.table.item(index, 3).text()
        self.student_middlename = QLineEdit(student_middlename)
        self.student_middlename.setPlaceholderText("Middlename")
        layout.addWidget(self.student_middlename)

        # Create a QLabel to serve as a textPlaceholder
        placeholder_label = QLabel("Birthdate (YYYY-DD-MM):")
        placeholder_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(placeholder_label)

        # Insert student birthday widget
        student_birthdate_text = student_management_sys.table.item(index, 4).text()
        date_format = "yyyy-dd-MM"
        student_birthdate = QDate.fromString(student_birthdate_text, date_format)
        self.student_birthdate = QDateEdit(student_birthdate)
        self.student_birthdate.setCalendarPopup(True)  # Enable the calendar popup
        self.student_birthdate.setDisplayFormat("yyyy-dd-MM")
        layout.addWidget(self.student_birthdate)

        # Create a QLabel to serve as a textPlaceholder
        placeholder_label = QLabel("Gender:")
        placeholder_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(placeholder_label)

        # Add student gender widget
        student_gender = student_management_sys.table.item(index, 5).text()
        self.student_gender = QComboBox()
        courses = ["Male", "Female"]
        self.student_gender.addItems(courses)
        self.student_gender.setCurrentText(student_gender)
        layout.addWidget(self.student_gender)

        # Add student address widget
        student_address = student_management_sys.table.item(index, 6).text()
        self.student_address = QLineEdit(student_address)
        self.student_address.setPlaceholderText("Address")
        layout.addWidget(self.student_address)

        # Add student guardian widget
        student_guardian = student_management_sys.table.item(index, 7).text()
        self.student_guardian = QLineEdit(student_guardian)
        self.student_guardian.setPlaceholderText("Guardian")
        layout.addWidget(self.student_guardian)

        # Add mobile widget
        student_mobile = student_management_sys.table.item(index, 8).text()
        self.student_mobile = QLineEdit(student_mobile)
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)

        # Add a submit button
        self.button = QPushButton("Update")
        self.button.clicked.connect(self.update_student)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def update_student(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            sql = "UPDATE student_info SET firstname = %s, lastname = %s, middlename = %s, birthdate = %s, gender = %s," \
                  "address = %s, guardian = %s, mobileno = %s" \
                  "WHERE pk_studentid = %s"
            cursor.execute(sql,
                           (self.student_firstname.text(), self.student_lastname.text(), self.student_middlename.text(),
                            self.student_birthdate.date().toString("yyyy-MM-dd"),
                            self.student_gender.itemText(self.student_gender.currentIndex()),
                            self.student_address.text(), self.student_guardian.text(), self.student_mobile.text(),
                            self.student_id))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, 'Success', 'Data updated successfully!')
            student_management_sys.load_data()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Data edit failed!')
            print(f"An error occurred: {e}")


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

    def delete_button(self):
        # Get select row index and student_id
        index = student_management_sys.table.currentRow()
        student_id = student_management_sys.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from student_info WHERE pk_studentid = %s", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        student_management_sys.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()


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
            student_management_sys.load_data()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Data insertion failed!')
            print(f"An error occurred: {e}")


class CheckRecord(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Record")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        # Create a QVBoxLayout to hold the widgets
        layout = QVBoxLayout()

        self.enroll_button = QPushButton("Enroll")
        # self.enroll_button.clicked.connect(self.enroll)
        self.enroll_button.setFixedSize(100, 40)  # Set the size of the button
        layout.addWidget(self.enroll_button)

        # Create a QTableWidget with 3 columns
        self.record_table = QTableWidget()
        self.record_table.setColumnCount(5)
        self.record_table.setHorizontalHeaderLabels(
            ["Student ID", "Assigned Teacher", "Time Schedule", "School Year", "Status"])

        # Add widgets to the layout
        layout.addWidget(self.record_table)

        # Set the layout for the dialog
        self.setLayout(layout)

        self.statusbar = QStatusBar()
        layout.addWidget(self.statusbar)

        self.load_record()
        # edit_dialog = EditRecordDialog(data)

        self.record_table.cellClicked.connect(self.cell_clicked)

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

    def load_record(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        global selected_record_id
        print(selected_record_id)

        sql = "SELECT fk_studentid, teacher, timesched, schoolyear, status FROM record_info WHERE fk_studentid = %s"
        cursor.execute(sql, (selected_record_id, ))
        result = cursor.fetchall()
        self.record_table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.record_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.record_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def edit(self):
        data = self.load_record()
        edit_dialog = EditRecordDialog(data)
        edit_dialog.exec()

    def delete(self):
        delete_dialog = DeleteRecordDialog()
        delete_dialog.exec()

    def enroll(self):
        enroll_dialog = EnrollStudentDialog()
        enroll_dialog.exec()
        print('enroll')


class EditRecordDialog(QDialog):
    def __init__(self, record):
        super().__init__()
        self.setWindowTitle("Update Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        self.record = record
        print(self.record)

        layout = QVBoxLayout()

        self.student_id = self.record[0][0]

        teacher_label = QLabel("Teacher Assigned:")
        teacher_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(teacher_label)

        self.teacher = QComboBox()
        self.assigned_teacher = self.record[0][1]
        teachers = ["Teacher 1", "Teacher 2"]
        self.teacher.addItems(teachers)
        self.teacher.setCurrentText(self.assigned_teacher)
        layout.addWidget(self.teacher)

        schedule_label = QLabel("Time Schedule:")
        schedule_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(schedule_label)

        self.time_schedule = QComboBox()
        self.schedule = self.record[0][2]
        schedule = ["8:00 AM - 10:00 AM", "10:00 AM - 12:00 NN"]
        self.time_schedule.addItems(schedule)
        self.time_schedule.setCurrentText(self.schedule)
        layout.addWidget(self.time_schedule)

        schoolyear_label = QLabel("School Year (YYYY-YYYY):")
        schoolyear_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(schoolyear_label)

        self.school_year_attend = self.record[0][3]
        self.school_year = QLineEdit(self.school_year_attend)
        self.school_year.setPlaceholderText("School Year")
        layout.addWidget(self.school_year)

        self.button = QPushButton("Update")
        self.button.clicked.connect(self.update_student_record)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def update_student_record(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            sql = "UPDATE record_info SET teacher = %s, timesched = %s, schoolyear = %s" \
                  "WHERE fk_studentid = %s"
            cursor.execute(sql,
                           (self.teacher.itemText(self.teacher.currentIndex()),
                            self.time_schedule.itemText(self.time_schedule.currentIndex()),
                            self.school_year.text(),
                            self.student_id))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, 'Success', 'Record updated successfully!')
            load_data = CheckRecord()
            load_data.load_record()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Record edit failed!')
            print(f"An error occurred: {e}")


class DeleteRecordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Record")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 1)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student_record)

    def delete_student_record(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()

            sql = "DELETE record_info WHERE fk_studentid = %s"
            cursor.execute(sql, (self.student_id,))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, 'Success', 'Record deleted successfully!')
            load_data = CheckRecord()
            load_data.load_record()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Record delete failed!')
            print(f"An error occurred: {e}")


class EnrollStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enroll Student")
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        index = student_management_sys.table.currentRow()
        student_firstname = student_management_sys.table.item(index, 1).text()

        teacher_label = QLabel("Teacher Assigned:")
        teacher_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(teacher_label)

        self.teacher = QComboBox()
        teachers = ["Teacher 1", "Teacher 2"]
        self.teacher.addItems(teachers)
        self.teacher.setCurrentText(self.teacher)
        layout.addWidget(self.teacher)

        schedule_label = QLabel("Time Schedule:")
        schedule_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(schedule_label)

        self.time_schedule = QComboBox()
        schedule = ["8:00 AM - 10:00 AM", "10:00 AM - 12:00 NN"]
        self.time_schedule.addItems(schedule)
        self.time_schedule.setCurrentText(self.time_schedule)
        layout.addWidget(self.time_schedule)

        schoolyear_label = QLabel("School Year (YYYY-YYYY):")
        schoolyear_label.setStyleSheet("color: gray;")  # Style it as a placeholder
        layout.addWidget(schoolyear_label)

        self.school_year = QLineEdit()
        self.school_year.setPlaceholderText("School Year")
        layout.addWidget(self.school_year)

        self.button = QPushButton("Enroll")
        self.button.clicked.connect(self.enroll_student())
        layout.addWidget(self.button)

        self.setLayout(layout)

    def enroll_student(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            sql = "INSERT INTO record_info (fk_studentid, teacher, timesched, schoolyear)" \
                  "VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql,
                           (self.student_number, self.teacher.itemText(self.teacher.currentIndex()),
                            self.time_schedule.itemText(self.time_schedule.currentIndex()),
                            self.school_year.text()))
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, 'Success', 'Record added successfully!')
            load_data = CheckRecord()
            load_data.load_record()
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Record adding failed!')
            print(f"An error occurred: {e}")

app = QApplication(sys.argv)
student_management_sys = MainWindow()
student_management_sys.show()
student_management_sys.load_data()
sys.exit(app.exec())
