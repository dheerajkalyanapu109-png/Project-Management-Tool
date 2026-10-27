from django.contrib import admin
from .models import Project, Task, Comment, Notification
for m in (Project, Task, Comment, Notification): admin.site.register(m)
