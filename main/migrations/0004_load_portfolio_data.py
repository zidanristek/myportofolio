"""Kept as a no-op so applied histories stay valid.

This migration used to load the fixtures. loaddata builds rows from the models
as they are today, not as they were when the migration was written, so once
later migrations added columns to Project the fixture no longer fitted the
table that existed at this point and a fresh database could not migrate at all.

The loading moved to the last migration, where the table always matches the
fixture. Databases that already ran this one are unaffected: a migration is
never applied twice.
"""

from django.db import migrations


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_experience_options_experience_position"),
    ]

    operations = [
        migrations.RunPython(noop, noop),
    ]
