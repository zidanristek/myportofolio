import os

from django.contrib import messages
from django.core import serializers
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project

OWNER = "Muhammad Sultan Zidan"


def _code_matches(given):
    """The delete buttons post a bare field, so they check the secret here."""
    expected = os.getenv("EDIT_PASSWORD", "")
    return bool(expected) and given == expected


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


def _matching_experiences(request):
    """Every experience, narrowed by the title in the query string if there is one."""
    experiences = Experience.objects.all()
    title_query = request.GET.get("title", "").strip()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    return experiences


def get_experiences_json(request):
    payload = serializers.serialize("json", _matching_experiences(request))
    return HttpResponse(payload, content_type="application/json")


def get_experiences_xml(request):
    payload = serializers.serialize("xml", _matching_experiences(request))
    return HttpResponse(payload, content_type="application/xml")


def show_experience(request):
    # Same round trip as the projects page: the template is handed objects
    # rebuilt from the JSON endpoint rather than rows straight off the queryset.
    response = get_experiences_json(request)
    experiences = [
        item.object
        for item in serializers.deserialize("json", response.content.decode("utf-8"))
    ]

    context = {
        "name": OWNER,
        "experience_list": experiences,
        "title_query": request.GET.get("title", "").strip(),
    }
    return render(request, "experience.html", context)


def _save_experience(form):
    """Turn the finished checkbox into a date and keep an existing one intact."""
    experience = form.save(commit=False)

    if form.cleaned_data["is_finished"]:
        if experience.ended_at is None:
            experience.ended_at = timezone.now()
    else:
        experience.ended_at = None

    experience.save()
    return experience


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        _save_experience(form)
        messages.success(request, "Pengalaman baru berhasil ditambahkan.")
        return redirect("main:show_experience")

    context = {
        "name": OWNER,
        "form": form,
        "heading": "Add Experience",
        "form_action": reverse("main:create_experience"),
        "submit_label": "Tambah Pengalaman",
    }
    return render(request, "experience_form.html", context)


def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        _save_experience(form)
        messages.success(request, "Pengalaman berhasil diperbarui.")
        return redirect("main:show_experience")

    context = {
        "name": OWNER,
        "form": form,
        "heading": "Edit Experience",
        "form_action": reverse("main:update_experience", args=[experience.id]),
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "experience_form.html", context)


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method != "POST":
        return redirect("main:show_experience")

    if not _code_matches(request.POST.get("password")):
        messages.error(request, "Kode akses salah, pengalaman tidak dihapus.")
        return redirect("main:show_experience")

    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus.")
    return redirect("main:show_experience")


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
        "heading": "Add Project",
        "form_action": reverse("main:create_project"),
        "submit_label": "Tambah Proyek",
    }
    return render(request, "projects_form.html", context)


def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui.")
        return redirect("main:show_projects")

    context = {
        "name": OWNER,
        "form": form,
        "heading": "Edit Project",
        "form_action": reverse("main:update_project", args=[project.id]),
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "projects_form.html", context)


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method != "POST":
        return redirect("main:show_projects")

    if not _code_matches(request.POST.get("password")):
        messages.error(request, "Kode akses salah, proyek tidak dihapus.")
        return redirect("main:show_projects")

    project.delete()
    messages.success(request, "Proyek berhasil dihapus.")
    return redirect("main:show_projects")
