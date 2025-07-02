import random

class Student():
    def __init__(self, name, gender, status="Очередь"):
        self.name = name
        self.gender = gender
        self.status = status

    def __repr__(self):
        return f"Students({self.name}, {self.gender})"
    
    def choose_answer(self, question):
        words = question.get_words()
        z = 1.618
        weightbd = []
        remaining = 1.0
        for n in range(len(words)):        
            weight = remaining / z
            weightbd.append(weight)
            remaining = remaining - weight
            n = n - 1 
        print(sum(weightbd))
        if len(weightbd) == len(words): 
            if self.gender == 'М':
                save_word = random.choices(words, weightsbd)
            else:
                save_word = random.choices(words, weightsbd)
        print(save_word)
        return save_word

class Examiner:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.students_handled = 0
        self.failed = 0
        self.work_time = 0.0
        self.current_student = "-"

    def __repr__(self):
        return f"Examiner({self.name}, {self.gender})"


class Question:
    def __init__(self, text):
        self.text = text.strip()  # удаление пробелов

    def get_words(self):
        return self.text.split()

    def __repr__(self):
        return f"Question({self.text})"


def read_examiner(path):
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


examiners = read_examiner("examiners.txt")
students = read_students("students.txt")
questions = read_questions("questions.txt")

for e in examiners:
    print(e)

for s in students:
    print(s)

for q in questions:
    print(q)
