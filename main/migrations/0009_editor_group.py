"""Create the Editor group.

The assignment expects accounts to be put into the group through the admin,
but the group itself has to exist first. Building it here means a fresh clone
and a fresh deployment both start with the same roles, instead of depending on
someone remembering to click through /admin.

The group holds the two change permissions and nothing else. That is the whole
definition of an editor: may correct what is already there, may not add or
remove anything.
"""

from django.contrib.auth.management import create_permissions
from django.db import migrations

GROUP = "Editor"
PERMISSIONS = ["change_experience", "change_project"]


def create_group(apps, schema_editor):
    # Permissions are written by a post_migrate signal, which only fires once
    # every migration has run. On a fresh database this one would otherwise
    # look for rows that do not exist yet and quietly build an empty group.
    app_config = apps.get_app_config("main")
    app_config.models_module = True
    create_permissions(app_config, apps=apps, verbosity=0)
    app_config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    group, _ = Group.objects.get_or_create(name=GROUP)
    group.permissions.set(
        Permission.objects.filter(
            codename__in=PERMISSIONS, content_type__app_label="main"
        )
    )


def drop_group(apps, schema_editor):
    apps.get_model("auth", "Group").objects.filter(name=GROUP).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_experience_starred_by"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_group, drop_group),
    ]
