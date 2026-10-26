from django.shortcuts import render
from django.utils import timezone


DAYS = (
    ("monday", "Monday"),
    ("tuesday", "Tuesday"),
    ("wednesday", "Wednesday"),
    ("thursday", "Thursday"),
    ("friday", "Friday"),
    ("saturday", "Saturday"),
    ("sunday", "Sunday"),
)

SCHEDULE = {
    "monday": [
        ("09:00", "10:30", "Python foundations", "Variables, data types & clean code", "Room 204", "Python"),
        ("10:45", "12:15", "Web development", "HTML, CSS & your first Django view", "Room 204", "Django"),
        ("13:15", "14:00", "Study hall", "Project time with instructor support", "Library", "Study"),
    ],
    "tuesday": [
        ("09:00", "10:30", "Algorithms & logic", "Flowcharts, loops & problem solving", "Room 204", "Practice"),
        ("10:45", "12:15", "JavaScript basics", "Events, functions & the DOM", "Room 204", "Web"),
        ("13:15", "14:00", "Code lab", "Build a small interactive project", "Computer lab", "Lab"),
    ],
    "wednesday": [
        ("09:00", "10:30", "Python foundations", "Functions, lists & dictionaries", "Room 204", "Python"),
        ("10:45", "12:15", "Databases", "SQL basics and data modeling", "Room 204", "Data"),
        ("13:15", "14:00", "Peer review", "Share work and give kind feedback", "Library", "Workshop"),
    ],
    "thursday": [
        ("09:00", "10:30", "Django workshop", "Models, templates & URL patterns", "Room 204", "Django"),
        ("10:45", "12:15", "Git & teamwork", "Branches, commits & collaboration", "Room 204", "Tools"),
        ("13:15", "14:00", "Project studio", "One-on-one project check-ins", "Computer lab", "Studio"),
    ],
    "friday": [
        ("09:00", "10:30", "Full-stack project", "Put this week's skills together", "Computer lab", "Project"),
        ("10:45", "11:30", "Show & tell", "Demo something you made this week", "Room 204", "Community"),
        ("11:30", "12:00", "Weekly wrap-up", "Celebrate wins and plan next week", "Room 204", "Advisory"),
    ],
    "saturday": [],
    "sunday": [],
}


def index(request):
    today = timezone.localdate().strftime("%A").lower()
    selected_day = request.GET.get("day", today).lower()
    if selected_day not in SCHEDULE:
        selected_day = today

    context = {
        "days": [
            {"slug": slug, "name": name, "is_today": slug == today}
            for slug, name in DAYS
        ],
        "selected_day": selected_day,
        "selected_day_name": dict(DAYS)[selected_day],
        "classes": SCHEDULE[selected_day],
        "class_count": len(SCHEDULE[selected_day]),
        "today": today,
    }
    return render(request, "main/index.html", context)
