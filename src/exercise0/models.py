import random

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
        if self.gender == 'М':
            save_word = random.choices(words, weight_bd)
        else:
            save_word = random.choices(words, list(reversed(weight_bd)))
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