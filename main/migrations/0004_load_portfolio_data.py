"""Load the portfolio rows as part of migrating.

PWS runs migrate during a build but never loaddata, and db.sqlite3 is not in
the repository, so without this step a fresh deployment serves two empty
pages. Keeping the data in fixtures rather than inline here means the same
rows can be reloaded by hand with loaddata whenever that is useful.
"""

from django.conf import settings
from django.core.management import call_command
from django.db import migrations

FIXTURES = ["experience", "project"]


def load(apps, schema_editor):
    if settings.TESTING:
        return
    call_command("loaddata", *FIXTURES)


def unload(apps, schema_editor):
    if settings.TESTING:
        return
    apps.get_model("main", "Experience").objects.all().delete()
    apps.get_model("main", "Project").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_experience_options_experience_position"),
    ]

    operations = [
        migrations.RunPython(load, unload),
    ]
