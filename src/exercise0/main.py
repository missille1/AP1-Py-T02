import random
import time
from queue import Queue 
from queue import Empty
import threading
from prettytable import PrettyTable 
from prettytable import DEFAULT
from models import Student
from models import Question
from models import Examiner
from visuals import update_display
from visuals import clear_console

def read_examiners(path):
    with open(path, encoding="utf-8") as f:
        tokens = f.read().split()
        return [Examiner(tokens[i], tokens[i + 1]) for i in range(0, len(tokens), 2)]


def read_students(path):
    with open(path, encoding="utf-8") as f:
        tokens = f.read().split()
        return [Student(tokens[i], tokens[i + 1]) for i in range(0, len(tokens), 2)]


def read_questions(path):
    with open(path, encoding="utf-8") as f:
        return [Question(line) for line in f if line.strip()] # if line.strip() — пропускаем пустые строки


examiners = read_examiners("examiners.txt")
students = read_students("students.txt")
questions = read_questions("questions.txt")
start_time = time.time()
global_start = time.time()
exam_finished = False
LOCK = threading.Lock()
exam_questions = random.sample(questions, 3)

student_queue = Queue()
for s in students:
    student_queue.put(s)

original_order = list(students)

display_thread = threading.Thread(target=update_display)
display_thread.start()

threads = []
for e in examiners:
    t = threading.Thread(target = e.run_exam, args=(student_queue, start_time, exam_questions))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
exam_finished = True
display_thread.join()

clear_console()

student_table = PrettyTable()

student_table.field_names = ["Студент", "Статус"]
for s in students:
    if s.status == 'Сдал':
        student_table.add_row([s.name, s.status])

for s in students:
    if s.status == 'Провалил':
        student_table.add_row([s.name, s.status])
print(student_table)

examiner_table = PrettyTable()
examiner_table.field_names = ["Экзаменатор", "Всего студентов", "Завалил", "Время работы"]
for e in examiners:
    examiner_table.add_row([e.name, e.students_handled, e.failed, f"{e.work_time:.2f}"])
print(examiner_table)

total_time = time.time() - start_time   
print(f"Время с момента начала экзамена и до момента и его завершения: {total_time:.2f}")
print(f"Имена лучших студентов: {best_student()}")
print(f"Имя лучших экзаменаторов: {best_examiner_names()}")
print(f"Имена студентов, которых после экзамена отчислят: {student_expelled()}")
print(f"Лучшие вопросы: {best_questions()}")
print(f"Вывод: {exam_status()}")
