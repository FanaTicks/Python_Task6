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
