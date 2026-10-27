from django.conf import settings
from django.db import models
U = settings.AUTH_USER_MODEL
STATUSES = [("todo", "To do"), ("doing", "In progress"), ("done", "Done")]

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    owner = models.ForeignKey(U, on_delete=models.CASCADE, related_name="owned")
    members = models.ManyToManyField(U, related_name="projects")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]
    def __str__(self): return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUSES, default="todo")
    assignee = models.ForeignKey(U, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned")
    created_by = models.ForeignKey(U, null=True, on_delete=models.SET_NULL, related_name="created_tasks")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["created"]
    def __str__(self): return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(U, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["created"]

class Notification(models.Model):
    user = models.ForeignKey(U, on_delete=models.CASCADE, related_name="notifications")
    text = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]
