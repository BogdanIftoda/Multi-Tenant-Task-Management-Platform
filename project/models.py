from django.db import models

from tenant.base_model import BaseModel


class BaseProjectModel(models.Model):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    PRIORITIES = {
        HIGH: "High",
        MEDIUM: "Medium",
        LOW: "Low",
    }

    PENDING = "P"
    PROGRESS = "I"
    COMPLETED = "C"

    STATUSES = {
        PENDING: "Pending",
        PROGRESS: "In Progress",
        COMPLETED: "Completed",
    }

    creator = models.ForeignKey('tenant.User', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(choices=PRIORITIES, default=LOW)
    status = models.CharField(max_length=1, choices=STATUSES, default=PENDING)

    class Meta:
        abstract = True


class Label(BaseModel):
    name = models.CharField(max_length=100)


class Project(BaseModel, BaseProjectModel):
    start_date = models.DateField(auto_now_add=True, null=True, blank=True)
    workers = models.ManyToManyField('tenant.User', related_name='projects', blank=True)

    def __str__(self):
        return self.title


class Task(BaseProjectModel):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField('tenant.User', related_name='assigned_to', blank=True)
    labels = models.ManyToManyField('project.Label', related_name='tasks', blank=True)
