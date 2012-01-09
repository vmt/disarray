from django.db import models
from taggit.managers import TaggableManager

TASK_STATUS_CHOICES = (
    ('new',     'New'),
    ('open',    'Open'),
    ('active',  'Active'),
    ('shelve',  'Shelved'),
    ('closed',  'Closed')
)

class Task(models.Model):
    title       = models.TextField(blank=False, null=False)
    text        = models.TextField()
    status      = models.CharField(max_length=32, default='new',
                                   choices=TASK_STATUS_CHOICES)
    createdon   = models.DateTimeField(auto_now_add=True)
    modifiedon  = models.DateTimeField(auto_now_add=True)
    viewedon    = models.DateTimeField(null=False)
    views       = models.IntegerField(default=1)
    tags        = TaggableManager(blank=True)


class TaskUpdate(models.Model):
    task        = models.ForeignKey(Task)
    createdon   = models.DateTimeField(auto_now_add=True)
    text        = models.TextField()
