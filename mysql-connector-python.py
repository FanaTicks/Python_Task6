import mysql.connector

# Параметри підключення до бази даних
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "mypassword",
    "database": "mydatabase"
}

# Створення підключення
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Створення таблиць
create_tables_queries = [
    """
    CREATE TABLE Employees (
        EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
        LastName VARCHAR(255) NOT NULL,
        FirstName VARCHAR(255) NOT NULL,
        MiddleName VARCHAR(255),
        Address VARCHAR(255),
        Phone CHAR(13) DEFAULT 'XXX-XXX-XXXX',
        Education ENUM('спеціальна', 'середня', 'вища'),
        DepartmentID INT,
        PositionID INT
    )
    """,
    """
    CREATE TABLE Departments (
        DepartmentID INT PRIMARY KEY AUTO_INCREMENT,
        DepartmentName VARCHAR(255) NOT NULL,
        Phone CHAR(13) DEFAULT 'XXX-XXX-XXXX',
        RoomNumber INT CHECK (RoomNumber BETWEEN 701 AND 710)
    )
    """,
    """
    CREATE TABLE Positions (
        PositionID INT PRIMARY KEY AUTO_INCREMENT,
        PositionName VARCHAR(255) NOT NULL,
        Salary DECIMAL(10, 2),
        BonusPercentage DECIMAL(5, 2)
    )
    """,
    """
    CREATE TABLE Projects (
        ProjectNumber INT PRIMARY KEY AUTO_INCREMENT,
        ProjectName VARCHAR(255) NOT NULL,
        CompletionDate DATE,
        FundingAmount DECIMAL(15, 2)
    )
    """,
    """
    CREATE TABLE ProjectExecution (
        ExecutionID INT PRIMARY KEY AUTO_INCREMENT,
        ProjectNumber INT,
        DepartmentID INT,
        StartDate DATE,
        FOREIGN KEY (ProjectNumber) REFERENCES Projects(ProjectNumber),
        FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
    )
    """
]

for query in create_tables_queries:
    cursor.execute(query)

# Закриття підключення
cursor.close()
connection.close()
