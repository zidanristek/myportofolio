import json
import os
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Nusantara Defense",
            description="Tower defense yang mengangkat mitologi Nusantara.",
            category="game",
            cover="img/projects/nusantara-defense.jpg",
            cover_alt="Tangkapan layar Nusantara Defense",
            tech_stack="Roblox Studio, Lua, Blender",
            position=1,
        )

    def test_projects_url_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_project_data_is_rendered(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "Roblox Game")
        self.assertContains(response, self.project.cover_alt)
        for tech in ["Roblox Studio", "Lua", "Blender"]:
            self.assertContains(response, tech)

    def test_project_model(self):
        self.assertEqual(str(self.project), "Nusantara Defense")
        self.assertEqual(self.project.tech_list, ["Roblox Studio", "Lua", "Blender"])

    def test_projects_are_ordered_by_position(self):
        Project.objects.create(
            title="SCERA", description="Membaca jadwal dari portal mahasiswa.",
            category="tool", cover="img/projects/scera.jpg",
            cover_alt="Tangkapan layar SCERA", tech_stack="C#, WinForms",
            position=0,
        )

        titles = list(Project.objects.values_list("title", flat=True))

        self.assertEqual(titles, ["SCERA", "Nusantara Defense"])

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_main_page_links_to_projects_without_listing_them(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, f'href="{reverse("main:show_projects")}"')
        self.assertNotContains(response, self.project.title)


class ProjectWriteTest(TestCase):
    """Adding, deleting, and the two data-delivery endpoints.

    EDIT_PASSWORD is patched per test rather than read from .env, so the suite
    passes on a machine that has never created one.
    """

    CODE = "kode-uji"

    def setUp(self):
        self.project = Project.objects.create(
            title="Nusantara Defense",
            description="Tower defense yang mengangkat mitologi Nusantara.",
            category="game",
            cover="img/projects/nusantara-defense.jpg",
            cover_alt="Tangkapan layar Nusantara Defense",
            tech_stack="Roblox Studio, Lua, Blender",
            position=1,
        )
        self.payload = {
            "title": "Pacilator",
            "description": "Menerjemahkan dokumen dan takarir.",
            "category": "tool",
            "tech_stack": "Python, PyQt5",
            "project_url": "",
            "project_image_url": "",
        }

    def test_form_page_is_accessible(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, "Kode Akses")

    def test_create_project_with_the_right_code(self):
        with patch.dict(os.environ, {"EDIT_PASSWORD": self.CODE}):
            response = self.client.post(
                reverse("main:create_project"),
                {**self.payload, "password": self.CODE},
            )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="Pacilator").exists())

    def test_new_project_goes_to_the_end(self):
        with patch.dict(os.environ, {"EDIT_PASSWORD": self.CODE}):
            self.client.post(
                reverse("main:create_project"),
                {**self.payload, "password": self.CODE},
            )

        self.assertEqual(Project.objects.get(title="Pacilator").position, 2)

    def test_create_project_with_the_wrong_code(self):
        with patch.dict(os.environ, {"EDIT_PASSWORD": self.CODE}):
            response = self.client.post(
                reverse("main:create_project"),
                {**self.payload, "password": "salah"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kode akses salah.")
        self.assertFalse(Project.objects.filter(title="Pacilator").exists())

    def test_projects_json_endpoint(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response["Content-Type"], "application/json")
        body = json.loads(response.content)
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["fields"]["title"], self.project.title)

    def test_projects_json_filters_by_title(self):
        Project.objects.create(
            title="SCERA", description="Membaca jadwal.", category="tool",
            tech_stack="C#", position=2,
        )

        response = self.client.get(reverse("main:get_projects_json"), {"title": "scera"})

        body = json.loads(response.content)
        self.assertEqual([row["fields"]["title"] for row in body], ["SCERA"])

    def test_projects_xml_endpoint(self):
        response = self.client.get(reverse("main:get_projects_xml"))

        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, "<django-objects")
        self.assertContains(response, self.project.title)

    def test_search_on_the_projects_page(self):
        response = self.client.get(reverse("main:show_projects"), {"title": "zzzz"})

        self.assertContains(response, "Tidak ada proyek dengan nama tersebut.")
        self.assertNotContains(response, self.project.description)

    def test_delete_link_survives_the_json_round_trip(self):
        # show_projects hands the template objects rebuilt from JSON rather than
        # rows from the database. The primary key has to come back with them or
        # every delete button on the page points nowhere.
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(
            response,
            reverse("main:delete_project", args=[self.project.id]),
        )

    def test_delete_project_with_the_right_code(self):
        with patch.dict(os.environ, {"EDIT_PASSWORD": self.CODE}):
            response = self.client.post(
                reverse("main:delete_project", args=[self.project.id]),
                {"password": self.CODE},
            )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_delete_project_with_the_wrong_code(self):
        with patch.dict(os.environ, {"EDIT_PASSWORD": self.CODE}):
            self.client.post(
                reverse("main:delete_project", args=[self.project.id]),
                {"password": "salah"},
            )

        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    def test_delete_ignores_get(self):
        with patch.dict(os.environ, {"EDIT_PASSWORD": self.CODE}):
            self.client.get(reverse("main:delete_project", args=[self.project.id]))

        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
