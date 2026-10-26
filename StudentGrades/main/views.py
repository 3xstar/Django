from django.shortcuts import render

students_data = {
    1: {
        "name": "Захар",
        "group": "РПО",
        "grades": {"Flask": 1, "Django": 1},
    },
    2: {
        "name": "Вадим",
        "group": "РПО",
        "grades": {"Flask": 5, "Django": 5},
    },
}


def students_list(request):
    students = students_data
    return render(request, "grades/students_list.html", {"students": students})


def student_info(request, student_id):
    student = students_data.get(student_id)
    if student is None:
        from django.http import Http404

        raise Http404("Student not found")
    return render(request, "grades/student_detail.html", {"student": student})