import sqlite3
connection = sqlite3.connect('files/database.db')
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS `study_levels`")
cursor.execute("DROP TABLE IF EXISTS `study_majors`")
cursor.execute("DROP TABLE IF EXISTS `study_types`")
cursor.execute("DROP TABLE IF EXISTS `students`")
cursor.execute("""CREATE TABLE IF NOT EXISTS `study_levels` (
               `level_id` integer primary key NOT NULL UNIQUE,
               `level_name` TEXT NOT NULL
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `study_majors` (
               `major_id` integer primary key NOT NULL UNIQUE,
               `major_name` TEXT NOT NULL
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `study_types` (
               `type_id` integer primary key NOT NULL UNIQUE,
               `type_name` TEXT NOT NULL
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `students` (
               `student_id` integer primary key NOT NULL UNIQUE,
               `level_id` INTEGER NOT NULL,
               `major_id` INTEGER NOT NULL,
               `type_id` INTEGER NOT NULL,
               `surname` TEXT NOT NULL,
               `name` TEXT NOT NULL,
               `patronymic` TEXT NOT NULL,
               `average_grade` INTEGER NOT NULL,
               FOREIGN KEY (`level_id`) REFERENCES `study_levels`(`level_id`),
               FOREIGN KEY (`major_id`) REFERENCES `study_majors`(`major_id`),
               FOREIGN KEY (`type_id`) REFERENCES `study_types`(`type_id`)
               );
               """)
data = open('files/data.txt', 'r', encoding = 'utf-8')
new_table = True
levels_df = []
majors_df = []
types_df = []
students_df = []
lines = data.readlines()
for line in lines:
    line = line[:-1]
    if new_table:
        current_table = line
        new_table = False
    elif line == 'table':
        new_table = True
    elif current_table == 'study_levels':
        levels_df.append(line.split(','))
    elif current_table == 'study_majors':
        majors_df.append(line.split(','))
    elif current_table == 'study_types':
        types_df.append(line.split(','))
    elif current_table == 'students':
        students_df.append(line.split(','))
cursor.executemany("INSERT OR IGNORE INTO `study_levels` (`level_id`, `level_name`) VALUES (?, ?)", levels_df)
cursor.executemany("INSERT OR IGNORE INTO `study_majors` (`major_id`, `major_name`) VALUES (?, ?)", majors_df)
cursor.executemany("INSERT OR IGNORE INTO `study_types` (`type_id`, `type_name`) VALUES (?, ?)", types_df)
cursor.executemany("INSERT OR IGNORE INTO `students` (`student_id`, `level_id`, `major_id`, `type_id`, `surname`, `name`, `patronymic`, `average_grade`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", students_df)
#requests
cursor.execute("""SELECT COUNT(s.`student_id`)
               FROM `students` s
               """)
answer = cursor.fetchone()
print('Request 1')
print(f"{answer[0]} students in total")
print("---")

cursor.execute("""SELECT m.`major_name`, COUNT(`student_id`)
               FROM `students` s
               JOIN `study_majors` m ON s.`major_id` = m.`major_id`
               GROUP BY m.`major_id`
               """)
answer = cursor.fetchall()
print('Request 2')
for i in range(len(answer)):
    print(f"{answer[i][1]} students for {answer[i][0]}")
print("---")

cursor.execute("""SELECT t.`type_name`, COUNT(`student_id`)
               FROM `students` s
               JOIN `study_types` t ON s.`type_id` = t.`type_id`
               GROUP BY t.`type_id`
               """)
answer = cursor.fetchall()
print('Request 3')
for i in range(len(answer)):
    print(f"{answer[i][1]} for {answer[i][0]}")
print("---")

cursor.execute("""SELECT m.`major_name`, ROUND(MAX(`average_grade`), 1), ROUND(MIN(`average_grade`), 1), ROUND(AVG(`average_grade`), 1)
               FROM `students` s
               JOIN `study_majors` m ON s.`major_id` = m.`major_id`
               GROUP BY m.`major_id`
               """)
answer = cursor.fetchall()
print('Request 4')
for i in range(len(answer)):
    print(f"MAX = {answer[i][1]}, MIN = {answer[i][2]}, AVG = {answer[i][3]} for {answer[i][0]}")
print("---")

cursor.execute("""SELECT l.`level_name`, t.`type_name`, m.`major_name`, ROUND(AVG(s.`average_grade`), 1)
               FROM `students` s
               JOIN `study_levels` l ON s.`level_id` = l.`level_id`
               JOIN `study_types` t ON s.`type_id` = t.`type_id`
               JOIN `study_majors` m ON s.`major_id` = m.`major_id`
               GROUP BY l.`level_id`, t.`type_id`, m.`major_id`
               """)
answer = cursor.fetchall()
print('Request 5')
for i in range(len(answer)):
    print(f"AVG = {answer[i][3]} for {answer[i][0]}, {answer[i][1]}, {answer[i][2]}")
print("---")

cursor.execute("""SELECT s.`surname`, s.`name`, s.`patronymic`, ROUND(s.`average_grade`, 1)
               FROM `students` s
               JOIN `study_majors` m ON s.`major_id` = m.`major_id`
               JOIN `study_types` t ON s.`type_id` = t.`type_id`
               WHERE m.`major_name` = 'Applied_Informatics' AND t.`type_name` = 'Full-time'
               ORDER BY s.`average_grade` DESC
               LIMIT 5
               """)
answer = cursor.fetchall()
print('Request 6')
for i in range(len(answer)):
    print(f"AVG = {answer[i][3]} for {answer[i][0]}, {answer[i][1]}, {answer[i][2]}")
print("---")

cursor.execute("""SELECT s.`student_id`, s.`surname`, s.`name`, s.`patronymic`
               FROM `students` s
               WHERE EXISTS (
               SELECT 1 
               FROM `students` s2 
               WHERE s2.`surname` = s.`surname` 
               AND s2.`student_id` != s.`student_id`
               )
               """)
answer = cursor.fetchall()
print('Request 7')
for i in range(len(answer)):
    print(f"Student {answer[i][0]}: {answer[i][1]}, {answer[i][2]}, {answer[i][3]}")
print("---")

cursor.execute("""SELECT s.`student_id`, s.`surname`, s.`name`, s.`patronymic`
               FROM `students` s
               WHERE EXISTS (
               SELECT 1 
               FROM `students` s2 
               WHERE s2.`surname` = s.`surname` AND s2.`name` = s.`name` AND s2.`patronymic` = s.`patronymic`
               AND s2.`student_id` != s.`student_id`
               )
               """)
answer = cursor.fetchall()
print('Request 8')
for i in range(len(answer)):
    print(f"Student {answer[i][0]}: {answer[i][1]}, {answer[i][2]}, {answer[i][3]}") # fix this one too

cursor.close()
connection.close()