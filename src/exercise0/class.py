import random
import time
from queue import Queue 
from queue import Empty
import threading
import os
from prettytable import PrettyTable 
from prettytable import DEFAULT

class Student():
    def __init__(self, name, gender, status="Очередь"):
        self.name = name
        self.gender = gender
        self.status = status
        self.exam_time = 0.0
        self.status = "Очередь"

    def __repr__(self):
        return f"Students({self.name}, {self.gender})"
    
    def choose_answer(self, question):
        words = question.get_words()
        z = 1.618
        weight_bd = []
        remaining = 1.0
        for _ in range(len(words)):        
            weight = remaining / z
            weight_bd.append(weight)
            remaining = remaining - weight
        # print(sum(weight_bd))
        if self.gender == 'М':
            save_word = random.choices(words, weight_bd)
        else:
            # print('girl')
            save_word = random.choices(words, list(reversed(weight_bd)))
        # print(save_word)
        return save_word

class Question:
    def __init__(self, text):
        self.text = text.strip()  # удаление пробелов
        self.correct_count = 0

    def get_words(self):
        return self.text.split()

    def __repr__(self):
        return f"Question({self.text})"


class Examiner:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.students_handled = 0
        self.failed = 0
        self.work_time = 0.0
        self.current_student = "-"
        self.on_lunch = False
        self.current_student = "-"

    def __repr__(self):
        return f"Examiner({self.name}, {self.gender})"    
    
    def choose_question(self, question):
        words = question.get_words()
        correct_answer = random.choice(words)
        all_correct_answer = []
        all_correct_answer.append(correct_answer)
        flag = True
        while flag:
            remaining = []
            remaining = [w for w in words if w not in all_correct_answer]
            if len(remaining) != 0:
                if random.random() < 1/3: 
                    new_answer = random.choice(remaining)
                    all_correct_answer.append(new_answer)
                else: 
                    flag = False
            else: 
                    flag = False
        return all_correct_answer
    
    def evaluate(self, student_answer, correct_answers, questions): # evaluate - оценивать
        mood = random.random()
        ex_passed = True
        if mood <= 1/8:
             ex_passed = False
        if mood >= 1/8 and mood <= 5/8:
            correct = 0
            wrong = 0
            for student_word, correct_list, q in zip(student_answer, correct_answers, questions):
                if student_word in correct_list:
                    correct += 1
                    q.correct_count += 1
                else:
                    wrong += 1
            if correct >= wrong:
                pass
            else:
                ex_passed = False
        else: 
             ex_passed = True
        return ex_passed
    
    def run_exam(self, student_queue: Queue, start_time: float, exam_questions: list[Question]):
        done = False
        while not done:
            student = None
            LOCK.acquire() # синхронизация потока, чтобы не взяли одного студента два экзаменатора
            if not student_queue.empty():
                student = student_queue.get_nowait()
                self.current_student = student.name
            LOCK.release()
            done = student is None # выход

            if not done and student:
                elapsed = time.time() - start_time

                if not self.on_lunch and elapsed > 30:
                    self.on_lunch = True
                    # print(f"{self.name} уходит на обед...")
                    time.sleep(random.uniform(12, 18))

                start_exam = time.time()

                student_answer = []
                correct_answers = []
                for q in exam_questions:
                    answer = student.choose_answer(q)[0]
                    student_answer.append(answer)
                    correct_answers.append(self.choose_question(q))
                l = len(self.name)
                duration = random.uniform(l - 1, l + 1)
                time.sleep(duration)

                ex_passed = self.evaluate(student_answer, correct_answers, exam_questions)

                exam_time = time.time() - start_exam
                student.exam_time = exam_time
                student.status = "Сдал" if ex_passed else "Провалил"
                self.work_time += exam_time

                # print(student_answer)
                # print(correct_answers)
                # print(ex_passed)
                # print(f"{self.name} закончил экзамен с {student.name}")

                self.students_handled += 1
                if not ex_passed:
                    self.failed += 1
                
                exam_finished = True
                self.current_student = "-"


    # def run_exam(self, student_queue: Queue, start_time: float):
    #     done = False
    #     while not done:
    #         student = None
    #         LOCK.acquire()
    #         if not student_queue.empty():
    #             student = student_queue.get_nowait()
    #         LOCK.release()
    #         done = student is None
    #         start_exam = time.time()
    #         if not done and student:
    #             elapsed = time.time() - start_time
    #             if not self.on_lunch and elapsed > 30:
    #                 self.on_lunch = True
    #                 print(f"{self.name} уходит на обед...")
    #                 time.sleep(random.uniform(12, 18))
    #             student_answer = []
    #             correct_answers = []
    #             for q in exam_questions:
    #                 answer = student.choose_answer(q)[0]
    #                 student_answer.append(answer)
    #                 correct_answers.append(self.choose_question(q))
    #                 exam_time = time.time() - start_exam
    #                 self.work_time += exam_time
    #             ex_passed = self.evaluate(student_answer, correct_answers)
    #             # duration = random.uniform(5, 7) + len(self.name)
    #             duration = random.uniform(5, 7) * (1 + len(e.name)/10)
    #             time.sleep(duration)
    #             print(student_answer)
    #             print(correct_answers)
    #             print(ex_passed)
    #             print(f"{self.name} закончил экзамен с {student.name}")
    #             self.students_handled += 1
    #             if not ex_passed:
    #                 self.failed += 1
    #             self.work_time += duration 


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

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_state(students, examiners, student_queue, start_time, original_order):
    clear_console()
    queue_students = list(student_queue.queue)
    queue_names = [s.name for s in queue_students]

    queued = queue_students

    in_exam = [s for s in original_order if s.status == 'Очередь' and s not in queued] # ищем тех кто в очереди и сравниваем со всем списком
    passed = [s for s in students if s.status == "Сдал"]
    failed = [s for s in students if s.status == "Провалил"]

    sorted_students = queued + in_exam + passed + failed
    
    student1_table = PrettyTable()
    student1_table.field_names = ["Студент", "Статус"]
    # print(f"{'Студент':<15} {'Статус':<10}")
    for s in sorted_students:
        # print(f"{s.name:<15} {s.status:<10}")
        student1_table.add_row([s.name, s.status])
    print(student1_table)

    examiner1_table = PrettyTable()
    examiner1_table.field_names = ["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы"]
    # print(f"{'Экзаменатор':<15} {'Текущий студент':<10} {'Всего студентов':<10} {'Завалил':<10} {'Время работы':<10}")
    for e in examiners:
        # print(f"{e.name:<20} {e.current_student:<13} {e.students_handled:<13} {e.failed:<10} {e.work_time:<10.2f}")
        examiner1_table.add_row([e.name, e.current_student, e.students_handled, e.failed, f"{e.work_time:<10.2f}"])
    print(examiner1_table)
    print(f"Осталось в очереди: {len([s for s in students if s.status == 'Очередь'])} из {len(students)}")
    print(f"Время с момента начала экзамена: {(time.time() - start_time):.2f}")
    
    return sorted_students

def update_display():
    while not exam_finished:
        draw_state(students, examiners, student_queue, start_time, original_order)
        time.sleep(0.5)

def best_student():
    best_student_dict = {}
    best_student_list = []
    for s in students:
        if s.status == "Сдал":
            best_student_dict[s] = s.exam_time
            # print(f"{s.name}: {s.exam_time:.2f}")
    for key, value in best_student_dict.items():
        if value == min(best_student_dict.values()):
            best_student_list.append(key.name)
    return ", ".join(best_student_list)

def student_expelled():
    student_expelled_dict = {}
    student_expelled_list = []
    for s in students:
        if s.status == "Провалил":
            student_expelled_dict[s] = s.exam_time
            print(f"{s.name}: {s.exam_time:.2f}")
    for key, value in student_expelled_dict.items():
        if value == min(student_expelled_dict.values()):
            student_expelled_list.append(key.name)
    return ", ".join(student_expelled_list) 

def best_examiner_names():
    proc_fail_dict = {}
    for e in examiners:
        if e.students_handled > 0:
            proc_fail_dict[e] = (e.failed*100)/e.students_handled
    best_examiner_names = []
    for key, value in proc_fail_dict.items():
        if value == min(proc_fail_dict.values()):
            best_examiner_names.append(key.name)
    return ", ".join(best_examiner_names)

def best_questions():
    best = []
    max_count = max(q.correct_count for q in questions)
    for q in questions:
        if q.correct_count == max_count:
            best.append(q.text)
            # print(f"{q.text} — {q.correct_count} правильных ответов")
    return ", ".join(best)

def exam_status():
    good = 0
    bad = 0
    for s in students:
        if s.status == "Сдал":
            good += 1
        else:
            bad += 1
    if good/(good + bad)*100 > 85:
        ex_passed = "экзамен удался"
    else:
        ex_passed = "экзамен не удался"
    return ex_passed

examiners = read_examiners("examiners.txt")
students = read_students("students.txt")
questions = read_questions("questions.txt")
start_time = time.time()
global_start = time.time()
LOCK = threading.Lock()
exam_finished = False
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
# print(f"{'Экзаменатор':<15} {'Всего студентов':<10} {'Завалил':<10} {'Время работы':<10}")
for e in examiners:
    # print(f"{e.name:<20} {e.students_handled:<13} {e.failed:<10} {e.work_time:<10.2f}")
    examiner_table.add_row([e.name, e.students_handled, e.failed, f"{e.work_time:.2f}"])
print(examiner_table)

total_time = time.time() - start_time
# print("___")
# # best_examiner()
# print("___")      
print(f"Время с момента начала экзамена и до момента и его завершения:{total_time:.2f}")
print(f"Имена лучших студентов:{best_student()}")
print(f"Имя лучших экзаменаторов:{best_examiner_names()}")
print(f"Имена студентов, которых после экзамена отчислят:{student_expelled()}")
print(f"Лучшие вопросы:{best_questions()}")
print(f"Вывод:{exam_status()}")
