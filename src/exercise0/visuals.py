import os
import time
from prettytable import PrettyTable

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_state(students, examiners, student_queue, start_time, original_order):
    clear_console()
    queue_students = list(student_queue.queue)
    # queue_names = [s.name for s in queue_students]

    queued = queue_students

    in_exam = [s for s in original_order if s.status == 'Очередь' and s not in queued] # ищем тех кто в очереди и сравниваем со всем списком
    passed = [s for s in students if s.status == "Сдал"]
    failed = [s for s in students if s.status == "Провалил"]

    sorted_students = queued + in_exam + passed + failed
    
    student1_table = PrettyTable()
    student1_table.field_names = ["Студент", "Статус"]
    for s in sorted_students:
        student1_table.add_row([s.name, s.status])
    print(student1_table)

    examiner1_table = PrettyTable()
    examiner1_table.field_names = ["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы"]
    for e in examiners:
        examiner1_table.add_row([e.name, e.current_student, e.students_handled, e.failed, f"{e.work_time:<10.2f}"])
    print(examiner1_table)
    print(f"Осталось в очереди: {len([s for s in students if s.status == 'Очередь'])} из {len(students)}")
    print(f"Время с момента начала экзамена: {(time.time() - start_time):.2f}")
    
    return sorted_students

def update_display(students, examiners, student_queue, start_time, original_order, exam_finished_event):
    while not exam_finished_event.is_set():
        draw_state(students, examiners, student_queue, start_time, original_order)
        time.sleep(0.2)
        # time.sleep(3000000)

def render_final_report(students, examiners, questions, start_time,
                        best_student, best_examiner_names, student_expelled,
                        best_questions, exam_status):
    clear_console()

     # --- Таблица студентов ---
    student_table = PrettyTable()
    student_table.field_names = ["Студент", "Статус"]
    for s in students:
        if s.status == 'Сдал':
            student_table.add_row([s.name, s.status])

    for s in students:
        if s.status == 'Провалил':
            student_table.add_row([s.name, s.status])
    print(student_table)

    # --- Таблица экзаменаторов ---
    examiner_table = PrettyTable()
    examiner_table.field_names = ["Экзаменатор", "Всего студентов", "Завалил", "Время работы"]
    for e in examiners:
        examiner_table.add_row([e.name, e.students_handled, e.failed, f"{e.work_time:.2f}"])
    print(examiner_table)

    # --- Метрики/итоги ---
    total_time = time.time() - start_time   
    print(f"Время с момента начала экзамена и до момента и его завершения: {total_time:.2f}")
    print(f"Имена лучших студентов: {best_student(students)}")
    print(f"Имя лучших экзаменаторов: {best_examiner_names(examiners)}")
    print(f"Имена студентов, которых после экзамена отчислят: {student_expelled(students)}")
    print(f"Лучшие вопросы: {best_questions(questions)}")
    print(f"Вывод: {exam_status(students)}")