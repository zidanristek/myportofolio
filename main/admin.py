from django.contrib import admin

from main.models import Experience, Project


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("position", "title", "category", "is_ongoing")
    list_filter = ("category",)
    search_fields = ("title", "description")
    ordering = ("position",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("position", "title", "category")
    list_filter = ("category",)
    search_fields = ("title", "description", "tech_stack")
    ordering = ("position",)
