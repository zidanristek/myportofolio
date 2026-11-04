from django.templatetags.static import static
from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    # The card needs what only the server knows: the label of the category,
    # whether the cover is a static file or a URL, and the split stack.
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    cover_url = serializers.SerializerMethodField()
    tech_list = serializers.ListField(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "category", "category_display",
            "tech_stack", "tech_list", "project_url", "project_image_url",
            "cover_url", "cover_alt",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "cover_alt"]

    # ProjectForm.clean_* do not run on this path, so the same rules live here.
    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate_tech_stack(self, value):
        return strip_tags(value).strip()

    def get_cover_url(self, obj):
        return static(obj.cover) if obj.cover else obj.project_image_url

    def get_star_count(self, obj):
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
