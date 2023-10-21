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

# Функція для виведення результатів запиту у форматованому вигляді
def execute_and_print(query, title):
    cursor.execute(query)
    print(title)
    columns = cursor.description
    for column in columns:
        print(column[0], end='\t')
    print("\n" + "-" * 40)
    for row in cursor.fetchall():
        print(*row, sep='\t')
    print("\n")

# Отримання списку усіх таблиць у базі даних
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# Виведення структури та даних кожної таблиці
for table in tables:
    table_name = table[0]

    # Виведення структури таблиці
    print(f"Структура таблиці {table_name}:")
    cursor.execute(f"DESCRIBE {table_name}")
    for row in cursor.fetchall():
        print(row)
    print("\n")

    # Виведення даних таблиці
    execute_and_print(f"SELECT * FROM {table_name}", f"Дані таблиці {table_name}:")

# Виконання інших запитів
execute_and_print("""
SELECT LastName, FirstName, MiddleName 
FROM Employees 
JOIN Positions ON Employees.PositionID = Positions.PositionID
WHERE Salary > 2000
ORDER BY LastName;
""", "Робітники з окладом більше 2000 грн:")

execute_and_print("""
SELECT Departments.DepartmentName, COALESCE(AVG(Positions.Salary), 0) 
FROM Departments
LEFT JOIN Employees ON Employees.DepartmentID = Departments.DepartmentID
LEFT JOIN Positions ON Employees.PositionID = Positions.PositionID
GROUP BY Departments.DepartmentName;
""", "Середня зарплатня в кожному відділі:")

department_id = 1
execute_and_print(f"""
SELECT Projects.ProjectName 
FROM Projects 
JOIN ProjectExecution ON Projects.ProjectNumber = ProjectExecution.ProjectNumber
WHERE ProjectExecution.DepartmentID = {department_id};
""", f"Проекти в відділі {department_id}:")

execute_and_print("""
SELECT Departments.DepartmentName, COUNT(Employees.EmployeeID)
FROM Employees 
JOIN Departments ON Employees.DepartmentID = Departments.DepartmentID
GROUP BY Departments.DepartmentName;
""", "Кількість працівників у кожному відділі:")

execute_and_print("""
SELECT LastName, FirstName, MiddleName, Salary, BonusPercentage, (Salary * BonusPercentage / 100) as BonusAmount
FROM Employees 
JOIN Positions ON Employees.PositionID = Positions.PositionID;
""", "Розмір премії для кожного співробітника:")

execute_and_print("""
SELECT 
    Departments.DepartmentName,
    SUM(CASE WHEN Education = 'спеціальна' THEN 1 ELSE 0 END) AS 'Спеціальна',
    SUM(CASE WHEN Education = 'середня' THEN 1 ELSE 0 END) AS 'Середня',
    SUM(CASE WHEN Education = 'вища' THEN 1 ELSE 0 END) AS 'Вища'
FROM Employees
JOIN Departments ON Employees.DepartmentID = Departments.DepartmentID
GROUP BY Departments.DepartmentName;
""", "Кількість робітників за освітою у кожному відділі:")

# Закриття підключення
cursor.close()
connection.close()
