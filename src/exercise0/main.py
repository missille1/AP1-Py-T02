import time
import threading
from queue import Queue
import random
from prettytable import PrettyTable
from models.entities import Examiner, Student, Question
from models.examiner_logic import run_exam
from visuals import update_display, render_final_report
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
    
    render_final_report(
        students=students,
        examiners=examiners,
        questions=questions,
        start_time=start_time,
        best_student=best_student,
        best_examiner_names=best_examiner_names,
        student_expelled=student_expelled,
        best_questions=best_questions,
        exam_status=exam_status,
    )


if __name__=="__main__":
    main()