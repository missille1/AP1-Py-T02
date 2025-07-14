from main 

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
            # print(f"{s.name}: {s.exam_time:.2f}")
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
