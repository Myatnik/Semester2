import sqlite3

connection = sqlite3.connect("../files/database.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS `jobs`")
cursor.execute("DROP TABLE IF EXISTS `employees`")
cursor.execute("DROP TABLE IF EXISTS `contracts`")
cursor.execute("DROP TABLE IF EXISTS `clients`")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `jobs` (
        `id_job` INTEGER PRIMARY KEY NOT NULL UNIQUE,
        `job` TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `employees` (
        `id_employee` INTEGER PRIMARY KEY NOT NULL UNIQUE,
        `surname` TEXT NOT NULL,
        `name` TEXT NOT NULL,
        `phone_employee` TEXT NOT NULL,
        `id_job` INTEGER NOT NULL,
        FOREIGN KEY(`id_job`) REFERENCES `jobs`(`id_job`)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `contracts` (
        `id_contract` INTEGER PRIMARY KEY NOT NULL UNIQUE,
        `id_client` INTEGER NOT NULL,
        `id_employee` INTEGER NOT NULL,
        `price` REAL NOT NULL,
        `completion_date` TEXT NOT NULL,
        `completion_mark` TEXT NOT NULL,
        FOREIGN KEY(`id_client`) REFERENCES `clients`(`id_client`),
        FOREIGN KEY(`id_employee`) REFERENCES `employees`(`id_employee`)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `clients` (
        `id_client` INTEGER PRIMARY KEY NOT NULL UNIQUE,
        `organization` TEXT NOT NULL,
        `phone_client` TEXT NOT NULL
    )
""")

data = open('../files/data.txt', 'r', encoding = 'utf-8')
new_table = True
jobs_df = []
employees_df = []
contracts_df = []
clients_df = []
lines = data.readlines()
for line in lines:
    line = line[:-1]
    if new_table:
        current_table = line
        new_table = False
    elif line == 'table_end':
        new_table = True
    elif current_table == 'jobs':
        jobs_df.append(line.split(','))
    elif current_table == 'employees':
        employees_df.append(line.split(','))
    elif current_table == 'contracts':
        contracts_df.append(line.split(','))
    elif current_table == 'clients':
        clients_df.append(line.split(','))
#
'''
print(jobs_df)
print(employees_df)
print(contracts_df)
print(clients_df)'''
cursor.executemany("INSERT OR IGNORE INTO `jobs` (`id_job`, `job`) VALUES (?, ?)", jobs_df)
cursor.executemany("INSERT OR IGNORE INTO `employees` (`id_employee`, `surname`, `name`, `phone_employee`, `id_job`) VALUES (?, ?, ?, ?, ?)", employees_df)
cursor.executemany("INSERT OR IGNORE INTO `contracts` (`id_contract`, `id_client`, `id_employee`, `price`, `completion_date`, `completion_mark`) VALUES (?, ?, ?, ?, ?, ?)", contracts_df)
cursor.executemany("INSERT OR IGNORE INTO `clients` (`id_client`, `organization`, `phone_client`) VALUES (?, ?, ?)", clients_df)

connection.commit()

print("---simple requests---")
cursor.execute("""SELECT e.`surname`, e.`name`
                FROM `employees` e
""")
answer = cursor.fetchall()
print("All employees:")
for i in range(len(answer)):
    print(f"{i+1}: {answer[i][0]} {answer[i][1]}")
print("---")

cursor.execute("""SELECT j.`job`
                FROM `jobs` j
""")
answer = cursor.fetchall()
print("All jobs:")
for i in range(len(answer)):
    print(f"{i+1}: {answer[i][0]}")
print("---")

cursor.execute("""SELECT c.`organization`
                FROM `clients` c
""")
answer = cursor.fetchall()
print("All clients:")
for i in range(len(answer)):
    print(f"{i+1}: {answer[i][0]}")
print("---")

cursor.execute("""SELECT c.`organization`, c.`phone_client`
                FROM `clients` c
""")
answer = cursor.fetchall()
print("Clients numbers:")
for i in range(len(answer)):
    print(f"{answer[i][0]}: {answer[i][1]}")
print("---")

cursor.execute("""SELECT e.`surname`, e.`name`, e.`phone_employee`
                FROM `employees` e
""")
answer = cursor.fetchall()
print("Employees numbers:")
for i in range(len(answer)):
    print(f"{answer[i][0]} {answer[i][1]}: {answer[i][2]}")

print()
print("---agregation requests---")

cursor.execute("""SELECT ROUND(SUM(co.`price`), 2), ROUND(SUM(CASE WHEN co.`completion_mark` = 'True' THEN co.`price` ELSE 0 END), 2) as received, ROUND(SUM(CASE WHEN co.`completion_mark` = 'False' THEN co.`price` ELSE 0 END), 2) as pending
                FROM `contracts` co
""")
answer = cursor.fetchall()
print(f"Expected income: {answer[0][0]}")
print(f"Received income: {answer[0][1]}")
print(f"Pending income: {answer[0][2]}")
print("---")

cursor.execute("""SELECT COUNT(j.`job`)
                FROM `jobs` j
""")
answer = cursor.fetchall()
print(f"Amount of jobs: {answer[0][0]}")
print("---")

cursor.execute("""SELECT COUNT(c.`organization`)
                FROM `clients` c
""")
answer = cursor.fetchall()
print(f"Amount of clients: {answer[0][0]}")

print()
print("---join requests---")

cursor.execute("""SELECT e.`surname`, e.`name`, j.`job`
                FROM `employees` e
                JOIN `jobs` j ON e.`id_job` = j.`id_job`
""")
answer = cursor.fetchall()
print("All employees:")
for i in range(len(answer)):
    print(f"{answer[i][0]} {answer[i][1]} is a/an {answer[i][2]}")
print("---")

cursor.execute("""SELECT co.`id_contract`, c.`organization`, e.`surname`, e.`name`, co.`price`, CASE WHEN co.`completion_mark` = 'True' THEN 'finished' ELSE 'unfinished' END as status
                FROM `contracts` co
                JOIN `employees` e ON co.`id_employee` = e.`id_employee`
                JOIN `clients` c ON co.`id_client` = c.`id_client`
""")
answer = cursor.fetchall()
print("All contracts:")
for i in range(len(answer)):
    print(f"Contract {answer[i][0]} with {answer[i][1]}, curated by manager {answer[i][2]} {answer[i][3]} with income of {answer[i][4]}, {answer[i][5]}")
print("---")

cursor.execute("""SELECT c.`organization`, COUNT(CASE WHEN co.`completion_mark` = 'True' THEN 1 ELSE NULL END) as completed, COUNT(CASE WHEN co.`completion_mark` = 'False' THEN 1 ELSE NULL END) as uncompleted
                FROM `contracts` co
                JOIN `clients` c ON co.`id_client` = c.`id_client`
                GROUP BY c.`id_client`
""")
answer = cursor.fetchall()
print("Contracts per client:")
for i in range(len(answer)):
    print(f"{answer[i][0]} with {answer[i][1]} completed and {answer[i][2]} uncompleted")

cursor.close()
connection.close()