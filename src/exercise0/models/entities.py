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
    