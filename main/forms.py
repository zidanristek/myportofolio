import os

from django.core.exceptions import ValidationError
from django.forms import (
    BooleanField,
    CharField,
    CheckboxInput,
    ModelForm,
    NumberInput,
    PasswordInput,
    Select,
    Textarea,
    TextInput,
    URLInput,
)

from main.models import Experience, Project


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


class ExperienceForm(ModelForm):
    """Adds or edits one entry in the experience carousel.

    started_at and ended_at are deliberately absent. The first is filled by the
    database on insert, and the second is a timestamp the writer should never
    have to type: the checkbox below records that something has finished and
    the view turns that into a date.
    """

    # The entries that ship with the repository point at a file under static,
    # so a form URLField would reject perfectly good values. A plain text field
    # accepts both that and a full URL.
    thumbnail = CharField(
        label="Gambar",
        required=False,
        widget=TextInput(
            attrs={"placeholder": "img/experience/nama-berkas.jpg atau https://..."}
        ),
        help_text="Jalur di dalam static, atau URL lengkap.",
    )

    is_finished = BooleanField(
        label="Sudah Selesai",
        required=False,
        widget=CheckboxInput(),
        help_text="Biarkan kosong kalau pengalaman ini masih berjalan.",
    )

    password = CharField(
        label="Kode Akses",
        widget=PasswordInput(attrs={"placeholder": "Kode akses pemilik"}),
        help_text="Hanya pemilik portofolio yang bisa mengubah daftar ini.",
    )

    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "position",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "position": "Urutan Tampil",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Fund Winner RISTEK Hackathon 2026",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamannya dalam dua atau tiga kalimat.",
                    "rows": 4,
                }
            ),
            "category": Select(),
            "position": NumberInput(
                attrs={
                    "min": 1,
                    "placeholder": "1 berarti tampil paling depan",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["is_finished"].initial = not self.instance.is_ongoing

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
