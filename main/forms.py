import os

from django.core.exceptions import ValidationError
from django.forms import CharField, ModelForm, PasswordInput, Textarea, TextInput, URLInput

from main.models import Project


class ProjectForm(ModelForm):
    """Adds a project from the browser.

    The site has no accounts yet, so anyone who finds the page could add or
    remove entries. A shared secret kept in the environment is not real
    authentication, but it stops the deployed portfolio from being a public
    notice board until sessions are covered.
    """

    password = CharField(
        label="Kode Akses",
        widget=PasswordInput(attrs={"placeholder": "Kode akses pemilik"}),
        help_text="Hanya pemilik portofolio yang bisa menambah proyek.",
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "category": "Kategori",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nusantara Defense",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan proyeknya dalam dua atau tiga kalimat.",
                    "rows": 4,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, PostgreSQL",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/zidanristek/nama-proyek",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

    def clean_password(self):
        given = self.cleaned_data["password"]
        expected = os.getenv("EDIT_PASSWORD", "")

        if not expected:
            raise ValidationError(
                "EDIT_PASSWORD belum diatur di environment, jadi form dimatikan."
            )
        if given != expected:
            raise ValidationError("Kode akses salah.")

        return given
