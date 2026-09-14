from django.shortcuts import render

from main.models import Experience, Project


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
        # Experience.Meta.ordering already fixes the order.
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    context = {
        "name": "Muhammad Sultan Zidan",
        # Project.Meta.ordering already fixes the order, so no order_by here.
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)
