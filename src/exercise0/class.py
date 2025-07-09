import random
import time
from queue import Queue 
from queue import Empty
import threading

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

class Examiner:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.students_handled = 0
        self.failed = 0
        self.work_time = 0.0
        self.current_student = "-"
        self.on_lunch = False

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
    
    def evaluate(self, student_answer, correct_answers): # evaluate - оценивать
        mood = random.random()
        ex_passed = True
        if mood <= 1/8:
             ex_passed = False
        if mood >= 1/8 and mood <= 5/8:
            correct = 0
            wrong = 0
            for student_word, correct_list in zip(student_answer, correct_answers):
                if student_word in correct_list:
                    correct += 1
                else:
                    wrong += 1
            if correct >= wrong:
                pass
            else:
                ex_passed = False
        else: 
             ex_passed = True
        return ex_passed
    
    def run_exam(self, student_queue: Queue, start_time: float):
        done = False
        while not done:
            student = None
            LOCK.acquire()
            if not student_queue.empty():
                student = student_queue.get_nowait()
            LOCK.release()
            done = student is None

            if not done and student:
                elapsed = time.time() - start_time

                if not self.on_lunch and elapsed > 30:
                    self.on_lunch = True
                    print(f"{self.name} уходит на обед...")
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

                ex_passed = self.evaluate(student_answer, correct_answers)

                exam_time = time.time() - start_exam
                student.exam_time = exam_time
                student.status = "Сдал" if ex_passed else "Провалил"
                self.work_time += exam_time

                print(student_answer)
                print(correct_answers)
                print(ex_passed)
                print(f"{self.name} закончил экзамен с {student.name}")

                self.students_handled += 1
                if not ex_passed:
                    self.failed += 1


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

class Question:
    def __init__(self, text):
        self.text = text.strip()  # удаление пробелов

    def get_words(self):
        return self.text.split()

    def __repr__(self):
        return f"Question({self.text})"


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
LOCK = threading.Lock()

exam_questions = random.sample(questions, 3)

print("--------------------FULLL---------------------")
student_queue = Queue()
for s in students:
    student_queue.put(s)

threads = []
for e in examiners:
    t = threading.Thread(target = e.run_exam, args=(student_queue, start_time))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(f"{'Студент':<15} {'Статус':<10}")
for s in students:
    print(f"{s.name:<10} {s.status:<10}")

print(f"{'Экзаменатор':<15} {'Всего студентов':<10} {'Завалил':<10} {'Время работы':<10}")
for e in examiners:
    print(f"{e.name:<20} {e.students_handled:<13} {e.failed:<10} {e.work_time:<10.2f}")

def best_student():
    exam_time_dict = {}
    for e in students:
        best_time.append(e.work_time)
    answer = min(best_time) # имя студента нада а не время
    return answer 

def best_examiner_names():
    proc_fail_dict = {}
    for e in examiners:
        proc_fail_dict[e] = (e.failed*100)/e.students_handled
    best_examiner_names = []
    for key, value in proc_fail_dict.items():
        if value == min(proc_fail_dict.values()):
            best_examiner_names.append(key.name)
    return ", ".join(best_examiner_names)

total_time = time.time() - start_time
print("___")
# best_examiner()
print("___")      
print(f"Время с момента начала экзамена и до момента и его завершения:{total_time:.2f}")
print(f"Имена лучших студентов:{best_student}")
print(f"Имя лучших экзаменаторов:{best_examiner_names()}")