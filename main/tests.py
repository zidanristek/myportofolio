import json

from django.contrib.auth.models import Group, User
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
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_the_page_ships_the_frame_without_the_cards(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, 'id="experience-track"')
        self.assertContains(response, 'id="loading"')

    def test_the_card_contents_come_from_the_endpoint(self):
        fields = json.loads(
            self.client.get(reverse("main:get_experiences_json")).content
        )[0]["fields"]

        self.assertEqual(fields["title"], self.experience.title)
        self.assertEqual(fields["description"], self.experience.description)
        self.assertEqual(fields["category"], "Part-Time")
        self.assertTrue(fields["is_ongoing"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        fields = json.loads(
            self.client.get(reverse("main:get_experiences_json")).content
        )[0]["fields"]

        self.assertFalse(self.experience.is_ongoing)
        self.assertFalse(fields["is_ongoing"])


class ProjectTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("pemilik", password="rahasia-uji")
        self.client.force_login(self.owner)
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

    def test_project_data_reaches_the_endpoint_the_page_reads(self):
        response = self.client.get(reverse("main:get_projects_json"))

        fields = json.loads(response.content)[0]["fields"]
        self.assertEqual(fields["title"], self.project.title)
        self.assertEqual(fields["description"], self.project.description)
        self.assertEqual(fields["category"], "Roblox Game")
        self.assertEqual(fields["cover_alt"], self.project.cover_alt)
        self.assertEqual(fields["tech_list"], ["Roblox Studio", "Lua", "Blender"])

    def test_a_static_cover_is_sent_as_a_url(self):
        response = self.client.get(reverse("main:get_projects_json"))

        cover = json.loads(response.content)[0]["fields"]["cover_url"]
        self.assertTrue(cover.endswith("img/projects/nusantara-defense.jpg"))
        self.assertTrue(cover.startswith("/"))

    def test_the_page_ships_the_frame_without_the_cards(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, 'id="grid"')
        self.assertNotContains(response, self.project.description)

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

    def test_empty_projects_endpoint(self):
        Project.objects.all().delete()

        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(json.loads(response.content), [])

    def test_main_page_links_to_projects_without_listing_them(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, f'href="{reverse("main:show_projects")}"')
        self.assertNotContains(response, self.project.title)


class ProjectWriteTest(TestCase):
    """Adding, deleting, and the two data-delivery endpoints.

    Every test signs in as the owner first, because writing portfolio data now
    needs both an account and superuser rights.
    """

    def setUp(self):
        self.owner = User.objects.create_superuser("pemilik", password="rahasia-uji")
        self.client.force_login(self.owner)
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

    def test_create_project_with_the_right_code(self):
        response = self.client.post(
            reverse("main:create_project"),
            self.payload,
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="Pacilator").exists())

    def test_new_project_goes_to_the_end(self):
        self.client.post(
            reverse("main:create_project"),
            self.payload,
        )

        self.assertEqual(Project.objects.get(title="Pacilator").position, 2)

    def test_a_registered_account_cannot_create(self):
        self.client.force_login(User.objects.create_user("warga", password="rahasia-uji"))

        response = self.client.post(reverse("main:create_project"), self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.filter(title="Pacilator").exists())

    def test_a_visitor_is_sent_to_the_login_page(self):
        self.client.logout()

        response = self.client.get(reverse("main:create_project"))

        self.assertRedirects(
            response, "/login/?next=" + reverse("main:create_project")
        )

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

    def test_search_that_matches_nothing(self):
        response = self.client.get(reverse("main:get_projects_json"), {"title": "zzzz"})

        self.assertEqual(json.loads(response.content), [])

    def test_the_endpoint_carries_the_key_every_action_url_needs(self):
        # The delete, edit and star buttons are built in the browser from this
        # key. Without it every one of them would point at nothing.
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(json.loads(response.content)[0]["pk"], str(self.project.id))

    def test_delete_project_with_the_right_code(self):
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id]),
            {},
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_a_registered_account_cannot_delete(self):
        self.client.force_login(User.objects.create_user("warga", password="rahasia-uji"))

        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    def test_delete_ignores_get(self):
        self.client.get(reverse("main:delete_project", args=[self.project.id]))

        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())


class ExperienceApiTest(TestCase):
    """The endpoint the experience page is about to build its cards from."""

    def setUp(self):
        self.magang = Experience.objects.create(
            title="Asisten Riset",
            description="Membantu penelitian dosen.",
            category="research",
            thumbnail="img/experience/riset.jpg",
            position=1,
        )
        self.lepas = Experience.objects.create(
            title="Desainer Lepas",
            description="Mengerjakan identitas visual.",
            category="freelance",
            thumbnail="https://contoh.test/desain.jpg",
            position=2,
        )
        self.url = reverse("main:get_experiences_json")

    def _fields(self, response):
        return [row["fields"] for row in json.loads(response.content)]

    def test_the_payload_carries_what_a_card_needs(self):
        fields = self._fields(self.client.get(self.url))[0]

        self.assertEqual(fields["title"], "Asisten Riset")
        self.assertEqual(fields["category"], "Research")
        self.assertEqual(fields["category_value"], "research")
        self.assertTrue(fields["is_ongoing"])
        self.assertEqual(fields["star_count"], 0)
        self.assertFalse(fields["is_starred"])

    def test_a_static_thumbnail_is_sent_as_a_url(self):
        # The stored value is a path inside static, which only the server can
        # turn into something the browser can ask for.
        fields = self._fields(self.client.get(self.url))[0]

        self.assertEqual(fields["thumbnail_url"], "/static/img/experience/riset.jpg")

    def test_a_full_url_thumbnail_is_left_alone(self):
        fields = self._fields(self.client.get(self.url))[1]

        self.assertEqual(fields["thumbnail_url"], "https://contoh.test/desain.jpg")

    def test_the_title_narrows_the_list(self):
        fields = self._fields(self.client.get(self.url, {"title": "riset"}))

        self.assertEqual([field["title"] for field in fields], ["Asisten Riset"])

    def test_the_category_narrows_the_list(self):
        fields = self._fields(self.client.get(self.url, {"category": "freelance"}))

        self.assertEqual([field["title"] for field in fields], ["Desainer Lepas"])

    def test_a_category_nobody_offers_is_ignored(self):
        fields = self._fields(self.client.get(self.url, {"category": "<script>"}))

        self.assertEqual(len(fields), 2)

    def test_the_two_filters_narrow_together(self):
        fields = self._fields(
            self.client.get(self.url, {"title": "desainer", "category": "research"})
        )

        self.assertEqual(fields, [])

    def test_the_star_state_answers_per_account(self):
        warga = User.objects.create_user("warga", password="rahasia-uji")
        self.magang.starred_by.add(warga)

        anonim = self._fields(self.client.get(self.url))[0]
        self.assertEqual(anonim["star_count"], 1)
        self.assertFalse(anonim["is_starred"])

        self.client.force_login(warga)
        masuk = self._fields(self.client.get(self.url))[0]
        self.assertTrue(masuk["is_starred"])


class ExperienceSearchTest(TestCase):
    """Searching happens in the browser now, so what the page has to get right
    is the delay and the form that no longer submits itself."""

    def setUp(self):
        Experience.objects.create(
            title="Project Officer URBAN 2026",
            description="Memimpin kepanitiaan acara.",
            category="volunteer",
            position=1,
        )
        Experience.objects.create(
            title="Asisten Riset",
            description="Membantu penelitian dosen.",
            category="research",
            position=2,
        )

    def test_the_page_waits_before_asking(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "const SEARCH_DELAY = 300")

    def test_the_search_form_does_not_reload_the_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, 'id="experience-search-form"')
        self.assertNotContains(response, 'form method="get"')

    def test_a_keyword_narrows_the_endpoint(self):
        body = json.loads(
            self.client.get(
                reverse("main:get_experiences_json"), {"title": "urban"}
            ).content
        )

        self.assertEqual([row["fields"]["title"] for row in body],
                         ["Project Officer URBAN 2026"])


class ExperienceCategoryFilterTest(TestCase):
    """The toolbar button that narrows the carousel to one kind of entry."""

    def setUp(self):
        Experience.objects.create(
            title="Asisten Riset",
            description="Membantu penelitian dosen.",
            category="research",
            position=1,
        )
        Experience.objects.create(
            title="Project Officer URBAN 2026",
            description="Memimpin kepanitiaan acara.",
            category="volunteer",
            position=2,
        )

    def test_the_page_offers_every_category(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, 'popovertarget="category-filter"')
        for value, label in Experience.EXPERIENCE_CHOICES:
            self.assertContains(response, 'data-category="%s"' % value)
            self.assertContains(response, label)

    def test_the_endpoint_narrows_to_one_category(self):
        body = json.loads(
            self.client.get(
                reverse("main:get_experiences_json"), {"category": "volunteer"}
            ).content
        )

        self.assertEqual([row["fields"]["title"] for row in body],
                         ["Project Officer URBAN 2026"])

    def test_a_keyword_and_a_category_narrow_together(self):
        body = json.loads(
            self.client.get(
                reverse("main:get_experiences_json"),
                {"title": "asisten", "category": "volunteer"},
            ).content
        )

        self.assertEqual(body, [])


class SharedScriptTest(TestCase):
    """escapeHtml used to live inside the script on the projects page. A second
    page now builds cards the same way, so it moved to a file every page loads.
    """

    def test_every_page_loads_the_shared_helper(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "js/dom.js")

    def test_the_projects_page_no_longer_carries_its_own_copy(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertNotContains(response, "function escapeHtml")
        self.assertContains(response, "escapeHtml(")


class ProjectAjaxCreateTest(TestCase):
    """The endpoint the modal posts to, which answers in JSON rather than
    redirecting, so the page can stay where it is."""

    def setUp(self):
        self.owner = User.objects.create_superuser("pemilik", password="rahasia-uji")
        Project.objects.create(
            title="Nusantara Defense",
            description="Tower defense mitologi Nusantara.",
            category="game",
            tech_stack="Roblox Studio, Lua",
            position=1,
        )
        self.url = reverse("main:create_project_ajax")
        self.payload = {
            "title": "Pacilator",
            "description": "Menerjemahkan dokumen dan takarir.",
            "category": "tool",
            "tech_stack": "Python, PyQt5",
            "project_url": "",
            "project_image_url": "",
        }

    def test_the_owner_creates_and_gets_the_new_key_back(self):
        self.client.force_login(self.owner)

        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 201)
        project = Project.objects.get(title="Pacilator")
        self.assertEqual(json.loads(response.content)["pk"], str(project.id))

    def test_a_new_project_still_lands_at_the_end(self):
        self.client.force_login(self.owner)

        self.client.post(self.url, self.payload)

        self.assertEqual(Project.objects.get(title="Pacilator").position, 2)

    def test_invalid_input_is_refused_with_the_field_errors(self):
        self.client.force_login(self.owner)

        response = self.client.post(self.url, dict(self.payload, title="   "))

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", json.loads(response.content)["errors"])
        self.assertFalse(Project.objects.filter(title__contains="Pacilator").exists())

    def test_a_title_made_only_of_a_tag_is_refused(self):
        self.client.force_login(self.owner)
        payload = dict(self.payload, title='<img src="x" onerror="alert(1)">')

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", json.loads(response.content)["errors"])
        self.assertEqual(Project.objects.count(), 1)

    def test_tags_are_stripped_from_the_text_that_is_kept(self):
        self.client.force_login(self.owner)
        payload = dict(
            self.payload,
            title="Pacilator <b>v2</b>",
            description="Menerjemahkan <script>alert(1)</script>dokumen.",
            tech_stack="Python, <i>PyQt5</i>",
        )

        self.client.post(self.url, payload)

        project = Project.objects.get(title__startswith="Pacilator")
        self.assertEqual(project.title, "Pacilator v2")
        self.assertEqual(project.description, "Menerjemahkan alert(1)dokumen.")
        self.assertEqual(project.tech_stack, "Python, PyQt5")

    def test_a_visitor_is_refused_in_json_rather_than_redirected(self):
        # A redirect would be followed by fetch, which would then be handed a
        # login page with status 200 and no way to tell that it failed.
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertFalse(Project.objects.filter(title="Pacilator").exists())

    def test_a_registered_account_is_refused(self):
        self.client.force_login(User.objects.create_user("warga", password="rahasia-uji"))

        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.filter(title="Pacilator").exists())

    def test_an_editor_is_refused_too(self):
        editor = User.objects.create_user("editor", password="rahasia-uji")
        editor.groups.add(Group.objects.get(name="Editor"))
        self.client.force_login(editor)

        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 403)

    def test_get_is_not_allowed(self):
        self.client.force_login(self.owner)

        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_the_modal_reaches_the_owner_alone(self):
        visitor = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(visitor, 'id="project-form"')

        self.client.force_login(self.owner)
        owner = self.client.get(reverse("main:show_projects"))
        self.assertContains(owner, 'id="project-form"')
        self.assertContains(owner, 'popovertarget="add-project-modal"')


class ExperienceWriteTest(TestCase):
    """Create, update, delete, and the two experience data endpoints."""

    def setUp(self):
        self.owner = User.objects.create_superuser("pemilik", password="rahasia-uji")
        self.client.force_login(self.owner)
        self.experience = Experience.objects.create(
            title="Fund Winner RISTEK Hackathon 2026",
            description="Biotopia memenangi hackathon dan mendapat pendanaan.",
            category="research",
            thumbnail="img/experience/ristek-hackathon.jpg",
            position=1,
        )
        self.payload = {
            "title": "Project Officer URBAN 2026",
            "description": "Memimpin kepanitiaan URBAN 2026 milik Clubban UI.",
            "category": "volunteer",
            "thumbnail": "img/experience/banyumas.jpg",
            "position": 2,
        }

    def test_create_page_is_accessible(self):
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Add Experience")

    def test_create_experience(self):
        response = self.client.post(
            reverse("main:create_experience"),
            self.payload,
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title=self.payload["title"]).exists())

    def test_a_registered_account_cannot_create(self):
        self.client.force_login(User.objects.create_user("warga", password="rahasia-uji"))

        response = self.client.post(reverse("main:create_experience"), self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Experience.objects.filter(title=self.payload["title"]).exists())

    def test_update_page_is_prefilled(self):
        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, "Edit Experience")

    def test_update_experience(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Judul Sudah Diubah",
                "description": self.experience.description,
                "category": "internship",
                "thumbnail": self.experience.thumbnail,
                "position": 3,
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Judul Sudah Diubah")
        self.assertEqual(self.experience.category, "internship")
        self.assertEqual(self.experience.position, 3)

    def test_update_does_not_create_a_second_row(self):
        self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            self.payload,
        )

        self.assertEqual(Experience.objects.count(), 1)

    def test_finished_checkbox_writes_and_clears_the_end_date(self):
        url = reverse("main:update_experience", args=[self.experience.id])

        self.client.post(
            url, {**self.payload, "is_finished": "on"}
        )
        self.experience.refresh_from_db()
        self.assertIsNotNone(self.experience.ended_at)
        self.assertFalse(self.experience.is_ongoing)

        self.client.post(url, self.payload)
        self.experience.refresh_from_db()
        self.assertIsNone(self.experience.ended_at)
        self.assertTrue(self.experience.is_ongoing)

    def test_experiences_json_endpoint(self):
        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertEqual(response["Content-Type"], "application/json")
        body = json.loads(response.content)
        self.assertEqual(body[0]["fields"]["title"], self.experience.title)

    def test_experiences_json_filters_by_title(self):
        Experience.objects.create(
            title="Programmer of Game Development",
            description="Divisi Game Development RISTEK.",
            category="volunteer",
            position=2,
        )

        response = self.client.get(
            reverse("main:get_experiences_json"), {"title": "programmer"}
        )

        self.assertEqual(len(json.loads(response.content)), 1)

    def test_experiences_xml_endpoint(self):
        response = self.client.get(reverse("main:get_experiences_xml"))

        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, "<django-objects")
        self.assertContains(response, self.experience.title)

    def test_the_page_carries_the_templates_the_script_fills_in(self):
        # The real keys only arrive as JSON, so the page ships one url per
        # action built around a dummy key for the script to substitute into.
        response = self.client.get(reverse("main:show_experience"))

        dummy = "00000000-0000-0000-0000-000000000000"
        self.assertContains(response, reverse("main:update_experience", args=[dummy]))
        self.assertContains(response, reverse("main:delete_experience", args=[dummy]))

    def test_delete_experience(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id]),
            {},
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_a_registered_account_cannot_delete(self):
        self.client.force_login(User.objects.create_user("warga", password="rahasia-uji"))

        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_delete_experience_ignores_get(self):
        self.client.get(reverse("main:delete_experience", args=[self.experience.id]))

        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())


class ProjectUpdateTest(TestCase):
    """The project page gained the same edit path as the experience page."""

    def setUp(self):
        self.owner = User.objects.create_superuser("pemilik", password="rahasia-uji")
        self.client.force_login(self.owner)
        self.project = Project.objects.create(
            title="SCERA",
            description="Membaca jadwal dari portal mahasiswa.",
            category="tool",
            cover="img/projects/scera.jpg",
            cover_alt="Tangkapan layar SCERA",
            tech_stack="C#, WinForms",
            position=1,
        )

    def test_update_page_is_prefilled(self):
        response = self.client.get(reverse("main:update_project", args=[self.project.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, "Edit Project")
        self.assertContains(response, self.project.title)

    def test_update_project(self):
        response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            {
                "title": "SCERA v2",
                "description": self.project.description,
                "category": "desktop",
                "tech_stack": "C#, WinForms, SQLite",
                "project_url": "",
                "project_image_url": "",
            },
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "SCERA v2")
        self.assertEqual(Project.objects.count(), 1)


class AuthenticationTest(TestCase):
    """Register, login, logout, and the cookie that login leaves behind."""

    def test_register_page_is_accessible(self):
        response = self.client.get(reverse("main:register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_creates_an_account(self):
        response = self.client.post(
            reverse("main:register"),
            {
                "username": "warga",
                "password1": "Portofolio2026!",
                "password2": "Portofolio2026!",
            },
        )

        self.assertRedirects(response, reverse("main:login"))
        self.assertTrue(User.objects.filter(username="warga").exists())

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("main:register"),
            {
                "username": "warga",
                "password1": "Portofolio2026!",
                "password2": "Berbeda2026!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="warga").exists())

    def test_login_signs_the_account_in(self):
        User.objects.create_user("warga", password="Portofolio2026!")

        response = self.client.post(
            reverse("main:login"),
            {"username": "warga", "password": "Portofolio2026!"},
        )

        self.assertRedirects(response, reverse("main:show_main"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get(username="warga").pk)

    def test_login_sets_the_last_login_cookie(self):
        User.objects.create_user("warga", password="Portofolio2026!")

        response = self.client.post(
            reverse("main:login"),
            {"username": "warga", "password": "Portofolio2026!"},
        )

        self.assertIn("last_login", response.cookies)

    def test_the_profile_page_shows_the_cookie(self):
        self.client.cookies["last_login"] = "2026-09-21 19:30:00"

        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "2026-09-21 19:30:00")

    def test_the_profile_page_copes_without_the_cookie(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "Belum ada sesi login")

    def test_login_rejects_a_wrong_password(self):
        User.objects.create_user("warga", password="Portofolio2026!")

        response = self.client.post(
            reverse("main:login"),
            {"username": "warga", "password": "salah"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_clears_the_session_and_the_cookie(self):
        User.objects.create_user("warga", password="Portofolio2026!")
        self.client.post(
            reverse("main:login"),
            {"username": "warga", "password": "Portofolio2026!"},
        )

        response = self.client.get(reverse("main:logout"))

        self.assertRedirects(response, reverse("main:show_main"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(response.cookies["last_login"].value, "")

    def test_the_login_page_offers_the_way_to_register(self):
        response = self.client.get(reverse("main:login"))

        self.assertContains(response, reverse("main:register"))

    def test_the_navbar_follows_the_session(self):
        anonymous = self.client.get(reverse("main:show_main"))
        self.assertContains(anonymous, reverse("main:login"))
        self.assertNotContains(anonymous, reverse("main:logout"))

        self.client.force_login(User.objects.create_user("warga", password="rahasia-uji"))
        signed_in = self.client.get(reverse("main:show_main"))

        self.assertContains(signed_in, "warga")
        self.assertContains(signed_in, reverse("main:logout"))


class StarTest(TestCase):
    """Starring is open to any account, unlike writing portfolio data."""

    def setUp(self):
        self.project = Project.objects.create(
            title="Nusantara Defense",
            description="Tower defense mitologi Nusantara.",
            category="game",
            tech_stack="Roblox Studio, Lua",
            position=1,
        )
        self.warga = User.objects.create_user("warga", password="rahasia-uji")
        self.url = reverse("main:toggle_star", args=[self.project.id])

    def test_a_visitor_is_sent_to_the_login_page(self):
        response = self.client.post(self.url)

        self.assertRedirects(response, "/login/?next=" + self.url)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_a_registered_account_can_star(self):
        self.client.force_login(self.warga)

        response = self.client.post(self.url)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertIn(self.warga, self.project.starred_by.all())

    def test_starring_twice_removes_the_star(self):
        self.client.force_login(self.warga)

        self.client.post(self.url)
        self.client.post(self.url)

        self.assertEqual(self.project.starred_by.count(), 0)

    def test_get_does_not_change_anything(self):
        self.client.force_login(self.warga)

        self.client.get(self.url)

        self.assertEqual(self.project.starred_by.count(), 0)

    def test_the_api_names_the_accounts_rather_than_their_ids(self):
        self.project.starred_by.add(self.warga)

        body = json.loads(self.client.get(reverse("main:get_projects_json")).content)

        fields = body[0]["fields"]
        self.assertEqual(fields["starred_by_names"], "warga")
        self.assertEqual(fields["star_count"], 1)
        self.assertNotIn("starred_by", fields)

    def test_the_api_answers_per_account(self):
        self.project.starred_by.add(self.warga)

        anonymous = json.loads(self.client.get(reverse("main:get_projects_json")).content)
        self.client.force_login(self.warga)
        signed_in = json.loads(self.client.get(reverse("main:get_projects_json")).content)

        self.assertFalse(anonymous[0]["fields"]["is_starred"])
        self.assertTrue(signed_in[0]["fields"]["is_starred"])

    def test_owner_controls_stay_out_of_the_page_for_everyone_else(self):
        # The buttons are assembled by the script from these two flags, so the
        # flags are what the page has to get right.
        visitor = self.client.get(reverse("main:show_projects"))
        self.assertContains(visitor, 'const IS_OWNER = "false"')

        self.client.force_login(self.warga)
        registered = self.client.get(reverse("main:show_projects"))
        self.assertContains(registered, 'const CAN_CHANGE = "false"')
        self.assertContains(registered, 'const IS_OWNER = "false"')

        self.client.force_login(User.objects.create_superuser("pemilik", password="rahasia-uji"))
        owner = self.client.get(reverse("main:show_projects"))
        self.assertContains(owner, 'const CAN_CHANGE = "true"')
        self.assertContains(owner, 'const IS_OWNER = "true"')


class EditorRoleTest(TestCase):
    """The four roles, checked on the server rather than in the markup.

    An editor corrects entries that already exist. Adding and removing them
    stays with the owner, so the two rights are tested apart from each other.
    """

    def setUp(self):
        self.experience = Experience.objects.create(
            title="Fund Winner RISTEK Hackathon 2026",
            description="Biotopia memenangi hackathon.",
            category="research",
            position=1,
        )
        self.project = Project.objects.create(
            title="Nusantara Defense",
            description="Tower defense mitologi Nusantara.",
            category="game",
            tech_stack="Roblox Studio, Lua",
            position=1,
        )
        self.payload = {
            "title": "Judul Sudah Diubah",
            "description": self.experience.description,
            "category": "internship",
            "thumbnail": "",
            "position": 1,
        }

        self.visitor_paths = {
            "create": reverse("main:create_experience"),
            "edit": reverse("main:update_experience", args=[self.experience.id]),
            "delete": reverse("main:delete_experience", args=[self.experience.id]),
        }

        self.regular = User.objects.create_user("biasa", password="rahasia-uji")
        self.editor = User.objects.create_user("editor", password="rahasia-uji")
        self.editor.groups.add(Group.objects.get(name="Editor"))
        self.owner = User.objects.create_superuser("pemilik", password="rahasia-uji")

    def test_the_editor_group_carries_only_the_change_permissions(self):
        codenames = set(
            Group.objects.get(name="Editor").permissions.values_list("codename", flat=True)
        )

        self.assertEqual(codenames, {"change_experience", "change_project"})

    def test_a_visitor_is_sent_to_the_login_page(self):
        for name, path in self.visitor_paths.items():
            with self.subTest(action=name):
                self.assertRedirects(self.client.get(path), "/login/?next=" + path)

    def test_a_regular_account_is_refused_everything(self):
        self.client.force_login(self.regular)

        for name, path in self.visitor_paths.items():
            with self.subTest(action=name):
                self.assertEqual(self.client.get(path).status_code, 403)

    def test_an_editor_may_change_but_not_create_or_delete(self):
        self.client.force_login(self.editor)

        self.assertEqual(self.client.get(self.visitor_paths["edit"]).status_code, 200)
        self.assertEqual(self.client.get(self.visitor_paths["create"]).status_code, 403)
        self.assertEqual(self.client.post(self.visitor_paths["delete"]).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_an_editor_change_actually_saves(self):
        self.client.force_login(self.editor)

        response = self.client.post(self.visitor_paths["edit"], self.payload)

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Judul Sudah Diubah")

    def test_the_owner_may_do_everything(self):
        self.client.force_login(self.owner)

        self.assertEqual(self.client.get(self.visitor_paths["create"]).status_code, 200)
        self.assertEqual(self.client.get(self.visitor_paths["edit"]).status_code, 200)
        self.assertRedirects(
            self.client.post(self.visitor_paths["delete"]),
            reverse("main:show_experience"),
        )

    def test_the_same_rules_cover_projects(self):
        edit = reverse("main:update_project", args=[self.project.id])
        delete = reverse("main:delete_project", args=[self.project.id])

        self.client.force_login(self.editor)
        self.assertEqual(self.client.get(edit).status_code, 200)
        self.assertEqual(self.client.post(delete).status_code, 403)

        self.client.force_login(self.regular)
        self.assertEqual(self.client.get(edit).status_code, 403)

    def test_the_page_offers_each_role_only_what_it_may_use(self):
        add = reverse("main:create_experience")

        # The buttons are assembled by the script from these two flags, so the
        # flags are what the page has to get right.
        self.client.force_login(self.regular)
        regular = self.client.get(reverse("main:show_experience"))
        self.assertContains(regular, 'const CAN_CHANGE = "false"')
        self.assertContains(regular, 'const IS_OWNER = "false"')
        self.assertNotContains(regular, add)

        self.client.force_login(self.editor)
        editor = self.client.get(reverse("main:show_experience"))
        self.assertContains(editor, 'const CAN_CHANGE = "true"')
        self.assertContains(editor, 'const IS_OWNER = "false"')
        self.assertNotContains(editor, add)

        self.client.force_login(self.owner)
        owner = self.client.get(reverse("main:show_experience"))
        self.assertContains(owner, 'const CAN_CHANGE = "true"')
        self.assertContains(owner, 'const IS_OWNER = "true"')
        self.assertContains(owner, add)


class ExperienceStarTest(TestCase):
    """Starring an experience, open to any signed-in account."""

    def setUp(self):
        self.experience = Experience.objects.create(
            title="Project Officer URBAN 2026",
            description="Memimpin kepanitiaan URBAN 2026.",
            category="volunteer",
            position=1,
        )
        self.warga = User.objects.create_user("warga", password="rahasia-uji")
        self.url = reverse("main:toggle_star_experience", args=[self.experience.id])

    def test_a_visitor_is_sent_to_the_login_page(self):
        self.assertRedirects(self.client.post(self.url), "/login/?next=" + self.url)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_a_registered_account_can_star(self):
        self.client.force_login(self.warga)

        self.assertRedirects(
            self.client.post(self.url), reverse("main:show_experience")
        )
        self.assertIn(self.warga, self.experience.starred_by.all())

    def test_one_star_per_account(self):
        self.client.force_login(self.warga)

        self.client.post(self.url)
        self.client.post(self.url)
        self.client.post(self.url)

        self.assertEqual(self.experience.starred_by.count(), 1)

    def test_get_does_not_change_anything(self):
        self.client.force_login(self.warga)

        self.client.get(self.url)

        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_the_count_and_the_state_reach_the_page(self):
        self.client.force_login(self.warga)
        self.client.post(self.url)

        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Unstar")
        self.assertContains(response, "star-count")

    def test_the_api_names_the_accounts_rather_than_their_ids(self):
        self.experience.starred_by.add(self.warga)

        body = json.loads(self.client.get(reverse("main:get_experiences_json")).content)

        fields = body[0]["fields"]
        self.assertEqual(fields["starred_by_names"], "warga")
        self.assertNotIn("starred_by", fields)
