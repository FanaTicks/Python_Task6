import mysql.connector
from datetime import datetime, timedelta
import random

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

# Заповнення таблиць даними
insert_data_queries = [
    """
    INSERT INTO Departments (DepartmentName, Phone, RoomNumber) VALUES
    ('програмування', '123-456-7890', 701),
    ('дизайну', '123-456-7891', 702),
    ('інформаційних технологій', '123-456-7892', 703)
    """,

    """
    INSERT INTO Positions (PositionName, Salary, BonusPercentage) VALUES
    ('інженер', 1500, 10),
    ('редактор', 1800, 12),
    ('програміст', 2500, 15)
    """
]

# Додавання 17 співробітників
for i in range(17):
    education = "'вища'" if i % 3 == 0 else "'середня'" if i % 3 == 1 else "'спеціальна'"
    insert_data_queries.append(f"""
    INSERT INTO Employees (LastName, FirstName, MiddleName, Address, Phone, Education, DepartmentID, PositionID) 
    VALUES
    ('Прізвище{i}', 'Ім''я{i}', 'По-батькові{i}', 'вул. Лісова, {i}', '123-456-78{90 if i < 10 else i}', 
    {education}, 
    {i % 3 + 1}, 
    {i % 3 + 1})
    """)

# Додавання 8 проектів
for i in range(8):
    insert_data_queries.append(f"""
    INSERT INTO Projects (ProjectName, CompletionDate, FundingAmount) 
    VALUES
    ('Проект {i+1}', '2024-0{i+1}-01', {10000 + i*1000})
    """)

for query in insert_data_queries:
    cursor.execute(query)

# Здійснення коміту для збереження змін
connection.commit()

# Отримання максимального номера проекту та ідентифікатора відділу
cursor.execute("SELECT MAX(ProjectNumber) FROM Projects")
max_project_number = cursor.fetchone()[0]

cursor.execute("SELECT MAX(DepartmentID) FROM Departments")
max_department_id = cursor.fetchone()[0]

# Заповнення таблиці ProjectExecution
for _ in range(17):
    project_number = random.randint(1, max_project_number)
    department_id = random.randint(1, max_department_id)
    start_date = datetime.today() - timedelta(days=random.randint(0, 365))

    cursor.execute("""
        INSERT INTO ProjectExecution (ProjectNumber, DepartmentID, StartDate)
        VALUES (%s, %s, %s)
    """, (project_number, department_id, start_date))

# Зберігання змін
connection.commit()

# Закриття підключення
cursor.close()
connection.close()
