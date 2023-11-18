# Maasin Child Development Center Registration System
This project is a registration system developed using PyQt6 for managing student records at the Maasin Child Development Center.

## Description
The system allows for the management of student information including their names, birthdates, genders, addresses, guardians, and contact details. It provides functionalities to insert new student records, update existing records, delete records, and search for specific student information.

## Requirements
To run this application, ensure you have the following installed:

1. Python 3.x
2. PyQt6
3. MySQL Connector/Python

## Installation and Setup
1. Clone or download the project repository.

2. Install Python 3.x if not already installed.

3. Install PyQt6 and MySQL Connector/Python using pip:

    - pip install PyQt6 mysql-connector-python
4. Ensure your MySQL server is running and configure the database connection details in the DatabaseConnection class (host, user, password, database).

5. Run the application:

    - python main.py

## Usage
Upon running the application, you'll be presented with the main window of the registration system. Here are the main functionalities:

__Add Student__: Allows insertion of new student records.

__Search__: Enables searching for specific student information based on first name.

__Edit Record__: Modify existing student records.

__Delete Record__: Remove student records from the system.

__About__: Provides information about the application.
