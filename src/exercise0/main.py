import time
import threading
from queue import Queue
import random
from prettytable import PrettyTable
from models.entities import Examiner, Student, Question
from models.examiner_logic import run_exam
from visuals import update_display, clear_console
from analytics import (
    best_student,
    best_examiner_names,
    student_expelled,
    best_questions,
    exam_status
)

def main():
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
    exam_finished_event = threading.Event() # устанавливаем TRUE пока идет экзамен
    # Создаем объект блокировки
    LOCK = threading.Lock()
    exam_questions = random.sample(questions, 3)

    student_queue = Queue()
    for s in students:
        student_queue.put(s)

    original_order = list(students)

    display_thread = threading.Thread(target=update_display, 
                                      args=(students, examiners, student_queue, start_time, original_order, exam_finished_event))
    display_thread.start()
    # Создание и запуск потоков для вызова функции 
    threads = []
    for e in examiners:
        t = threading.Thread(target = run_exam, args=(e, student_queue, start_time, exam_questions, LOCK, exam_finished_event))
        t.start()
        threads.append(t)
    # Ожидание завершения всех потоков
    for t in threads:
        t.join()
    exam_finished_event.set()
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
    print(f"Имена лучших студентов: {best_student(students)}")
    print(f"Имя лучших экзаменаторов: {best_examiner_names(examiners)}")
    print(f"Имена студентов, которых после экзамена отчислят: {student_expelled(students)}")
    print(f"Лучшие вопросы: {best_questions(questions)}")
    print(f"Вывод: {exam_status(students)}")


if __name__=="__main__":
    main()