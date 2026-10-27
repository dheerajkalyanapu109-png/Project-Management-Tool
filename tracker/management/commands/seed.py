from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from tracker.models import Project, Task, Comment
class Command(BaseCommand):
    help = "Create demo users alice and bob (password demo12345) and a sample project"
    def handle(self, *a, **k):
        users = {}
        for n in ("alice", "bob"):
            u, new = User.objects.get_or_create(username=n)
            if new: u.set_password("demo12345"); u.save()
            users[n] = u
        if Project.objects.filter(name="Website Redesign").exists(): return self.stdout.write("Already seeded.")
        p = Project.objects.create(name="Website Redesign", description="Refresh the marketing site", owner=users["alice"])
        p.members.add(*users.values())
        t1 = Task.objects.create(project=p, title="Design new homepage", status="doing", assignee=users["bob"], created_by=users["alice"])
        Task.objects.create(project=p, title="Write launch copy", status="todo", assignee=users["alice"], created_by=users["alice"])
        Task.objects.create(project=p, title="Pick colour palette", status="done", assignee=users["bob"], created_by=users["alice"])
        Comment.objects.create(task=t1, author=users["alice"], text="Can we get a first draft by Friday?")
        self.stdout.write("Seeded: alice / bob, password demo12345.")
