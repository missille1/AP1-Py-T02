import random
import time
from threading import Lock
from queue import Queue
from models.entities import Examiner, Question

def choose_question(examiner: Examiner, question):
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
    
def evaluate(examiner: Examiner, student_answer: list[str], correct_answers: list[list[str]], questions): # evaluate - оценивать
    correct = 0
    wrong = 0
    for student_word, correct_list, q in zip(student_answer, correct_answers, questions):
        if student_word in correct_list:
            correct += 1
            q.correct_count += 1
        else:
            wrong += 1
    if correct >= wrong:
        ex_passed =  True
    else:
        ex_passed = False
    return ex_passed

def run_exam(examiner: Examiner, student_queue: Queue, start_time: float, exam_questions: list[Question], lock: Lock, exam_finished_event):
    done = False
    while not done:
        student = None
        lock.acquire() # синхронизация потока, чтобы не взяли одного студента два экзаменатора
        if not student_queue.empty():
            student = student_queue.get_nowait()
            examiner.current_student = student.name
        lock.release()
        done = student is None # выход

        if not done and student:
            elapsed = time.time() - start_time

            if not examiner.on_lunch and elapsed > 30:
                examiner.on_lunch = True
                # print(f"{examiner.name} уходит на обед...")
                time.sleep(random.uniform(12, 18))

            start_exam = time.time()
            mood = random.random()
            l = len(examiner.name)

            if mood < 1/8:
                ex_passed = False  # сразу завалил
                # print("Плохое настроение: сразу завалил")
                # print(f"DEBUG mood={mood:.3f}")
                student_answer = []
                correct_answers = []
                duration = random.uniform(l - 1, l + 1)  
            elif mood < 3/8:
                ex_passed = True  # сразу сдал
                # print("Хорошее настроение: сразу сдал")
                student_answer = []
                correct_answers = []
                duration = random.uniform(l - 1, l + 1)
            else:
                # print("Нейтральное настроение: оцениваем по вопросам")
                student_answer = []
                correct_answers = []
                for q in exam_questions:
                    answer = student.choose_answer(q)[0]
                    student_answer.append(answer)
                    correct_answers.append(choose_question(examiner, q))
                duration = random.uniform(l - 1, l + 1)
                ex_passed = evaluate(examiner, student_answer, correct_answers, exam_questions)

            time.sleep(duration)

            exam_time = time.time() - start_exam
            student.exam_time = exam_time
            student.status = "Сдал" if ex_passed else "Провалил"
            examiner.work_time += exam_time

            # print(student_answer)
            # print(correct_answers)
            # print(ex_passed)
            # print(f"{examiner.name} закончил экзамен с {student.name}")

            examiner.students_handled += 1
            if not ex_passed:
                examiner.failed += 1
            
            # exam_finished_event.set()
            examiner.current_student = "-"