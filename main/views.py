import os

from django.contrib import messages
from django.core import serializers
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ProjectForm
from main.models import Experience, Project

OWNER = "Muhammad Sultan Zidan"


def show_main(request):
    context = {
        "name": OWNER,
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
        "name": OWNER,
        # Experience.Meta.ordering already fixes the order.
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def _matching_projects(request):
    """Every project, narrowed by the title in the query string if there is one."""
    projects = Project.objects.all()
    title_query = request.GET.get("title", "").strip()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    return projects


def get_projects_json(request):
    payload = serializers.serialize("json", _matching_projects(request))
    return HttpResponse(payload, content_type="application/json")


def get_projects_xml(request):
    payload = serializers.serialize("xml", _matching_projects(request))
    return HttpResponse(payload, content_type="application/xml")


def show_projects(request):
    # The page reads its own JSON endpoint rather than the queryset. Going out
    # and back looks like a detour on one server, and it is, but it is the shape
    # the page keeps once the list is fetched by JavaScript or by a separate
    # client, and it proves the endpoint returns what the page needs.
    response = get_projects_json(request)
    projects = [
        item.object
        for item in serializers.deserialize("json", response.content.decode("utf-8"))
    ]

    context = {
        "name": OWNER,
        "project_list": projects,
        "title_query": request.GET.get("title", "").strip(),
    }
    return render(request, "projects.html", context)


def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        # New rows land at the end. Left at the default of 0 they would jump
        # ahead of the six the ordering was curated for.
        last = Project.objects.aggregate(Max("position"))["position__max"] or 0
        project.position = last + 1
        project.save()

        messages.success(request, "Proyek baru berhasil ditambahkan.")
        return redirect("main:show_projects")

    context = {
        "name": OWNER,
        "form": form,
    }
    return render(request, "projects_form.html", context)


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method != "POST":
        return redirect("main:show_projects")

    expected = os.getenv("EDIT_PASSWORD", "")

    if not expected or request.POST.get("password") != expected:
        messages.error(request, "Kode akses salah, proyek tidak dihapus.")
        return redirect("main:show_projects")

    project.delete()
    messages.success(request, "Proyek berhasil dihapus.")
    return redirect("main:show_projects")
