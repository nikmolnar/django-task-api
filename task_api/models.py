from uuid import uuid4

from django.db import models


class TaskInfo(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed')
    )

    uuid = models.UUIDField(default=uuid4)
    task = models.CharField(max_length=256)
    backend_data = models.TextField(null=True)
    status = models.CharField(max_length=16, default='pending', choices=STATUS_CHOICES)
    progress = models.IntegerField(null=True)
    target = models.IntegerField(null=True)
    inputs = models.TextField(default='{}')
    outputs = models.TextField(default='{}')
    messages = models.TextField(default='[]')
    created = models.DateTimeField()
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
