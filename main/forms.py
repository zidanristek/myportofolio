from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import (
    BooleanField,
    CharField,
    CheckboxInput,
    ModelForm,
    NumberInput,
    Select,
    Textarea,
    TextInput,
    URLInput,
)

from django.utils.html import strip_tags

from main.models import Experience, Project


class SignUpForm(UserCreationForm):
    """Keeps the two password boxes next to each other.

    UserCreationForm hangs the password rules off the first box, which pushes
    the confirmation a whole list away from the field it confirms. The rules
    read just as well under the second box.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rules = self.fields["password1"].help_text
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = rules


class ProjectForm(ModelForm):
    """Adds or edits one project. Only the portfolio owner reaches this form."""


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

    # Tags are stripped on the way in as a second line of defence. The first is
    # the escaping the projects page does before it writes a card, and that one
    # matters more: this only reaches rows saved from here on, and Django's own
    # documentation says the result of strip_tags is not guaranteed safe to
    # render as HTML.

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()



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

