"""Load the portfolio rows.

PWS runs migrate during a build but never loaddata, and db.sqlite3 is not in
the repository, so without this step a fresh deployment serves empty pages.

This has to stay the last migration that touches these tables. loaddata reads
the current models, so the columns it writes only exist once every schema
migration ahead of it has run.
"""

from django.conf import settings
from django.core.management import call_command
from django.db import migrations

FIXTURES = ["experience", "project"]


def load(apps, schema_editor):
    # Tests build the rows they need themselves, and several of them assert on
    # an empty table.
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
        ("main", "0009_editor_group"),
    ]

    operations = [
        migrations.RunPython(load, unload),
    ]
