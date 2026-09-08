from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Muhammad Sultan Zidan",
        "npm": "2506534876",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Computer Science student at Universitas Indonesia, class of 2025, "
            "now in my second year at Fasilkom. My interests sit where software "
            "meets visual work."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Muhammad Sultan Zidan",
        # Tanpa order_by, urutan baris diserahkan ke basis data. SQLite lokal
        # kebetulan mengembalikan urutan masuk, PostgreSQL di PWS belum tentu.
        "experience_list": Experience.objects.all().order_by("-started_at"),
    }
    return render(request, "experience.html", context)
