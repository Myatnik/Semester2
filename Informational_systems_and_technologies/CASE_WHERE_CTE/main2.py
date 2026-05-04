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
cursor.execute("""SELECT s.`surname`, s.`name`, CASE WHEN s.`average_grade` > 4.0 THEN 'cool' ELSE 'not cool' END as coolness, s.average_grade
                FROM `students` s
                WHERE s.`average_grade` > 4.0
""")
answer = cursor.fetchall()
print("Cool students: ")
for i in range(len(answer)):
    print(f"{answer[i][2]} student {answer[i][0]} {answer[i][1]}, average grade = {answer[i][3]}")
print("---")

cursor.execute("""SELECT s.`surname`, s.`name`, CASE WHEN s.`average_grade` > 4.0 THEN 'cool' ELSE 'not cool' END as coolness, s.average_grade
                FROM `students` s
                WHERE s.`average_grade` <= 4.0
""")
answer = cursor.fetchall()
print("Not cool students: ")
for i in range(len(answer)):
    print(f"{answer[i][2]} student {answer[i][0]} {answer[i][1]}, average grade = {answer[i][3]}")
print("---")

cursor.execute("""SELECT s.`surname`, s.`name`, s.`average_grade`
                FROM `students` s
                WHERE s.`average_grade` > (SELECT AVG(s.`average_grade`) FROM `students` s)
""")
answer = cursor.fetchall()
print("Students with grade above average in group:")
for i in range (len(answer)):
    print(f"{answer[i][0]} {answer[i][1]} with grade of {answer[i][2]}")
print("---")

cursor.execute("""SELECT s.`surname`, s.`name`, s.`average_grade`
                FROM `students` s
                WHERE s.`average_grade` < (SELECT AVG(s.`average_grade`) FROM `students` s)
""")
answer = cursor.fetchall()
print("Vice versa:")
for i in range (len(answer)):
    print(f"{answer[i][0]} {answer[i][1]} with grade of {answer[i][2]}")
print("---")

cursor.execute("""WITH worst_students as (
               SELECT s.`surname`, s.`name`, s.`average_grade`
               FROM `students` s
               ORDER BY s.`average_grade`
               LIMIT 5
               )
               SELECT *
               FROM worst_students""")
answer = cursor.fetchall()
print('Worst students:')
for i in range (len(answer)):
    print(f'{answer[i][2]}, {answer[i][0]} {answer[i][1]}')
print("---")

cursor.execute("""WITH best_students as (
               SELECT s.`surname`, s.`name`, s.`average_grade`
               FROM `students` s
               ORDER BY s.`average_grade` DESC
               LIMIT 5
               )
               SELECT *
               FROM best_students""")
answer = cursor.fetchall()
print('Best students:')
for i in range (len(answer)):
    print(f'{answer[i][2]}, {answer[i][0]} {answer[i][1]}')

cursor.close()
connection.close()