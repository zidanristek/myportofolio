import uuid

from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        # The carousel order is chosen, not chronological, so it is stored.
        # Deriving it from started_at would mean bending the real dates.
        ordering = ['position']

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('game', 'Roblox Game'),
        ('web', 'Web'),
        ('desktop', 'Windows App'),
        ('mobile', 'Mobile App'),
        ('tool', 'Desktop Tool'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web')
    cover = models.CharField(max_length=255)
    cover_alt = models.CharField(max_length=255)
    tech_stack = models.CharField(max_length=255)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        # The order is curated rather than chronological, so it is stored
        # instead of derived. Ordering on the model keeps the view a plain
        # objects.all() and stops PostgreSQL returning rows in its own order.
        ordering = ['position']

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        """Split the stored stack into the tags the template renders."""
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]
