from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Project, Task, Comment, STATUSES
from .realtime import broadcast, notify

def _project(request, pk):
    return get_object_or_404(Project.objects.filter(members=request.user), pk=pk)

def _task(request, pk):
    return get_object_or_404(Task.objects.select_related("project", "assignee"), pk=pk, project__members=request.user)

def _assignee(project, raw):
    return project.members.filter(pk=raw).first() if raw else None

@login_required
def dashboard(request):
    projects = request.user.projects.annotate(n_tasks=Count("tasks", distinct=True))
    return render(request, "dashboard.html", {"projects": projects})

@require_POST
@login_required
def project_create(request):
    name = request.POST.get("name", "").strip()
    if not name:
        messages.error(request, "Give the project a name."); return redirect("dashboard")
    p = Project.objects.create(name=name, description=request.POST.get("description", "").strip(), owner=request.user)
    p.members.add(request.user)
    return redirect("project_detail", pk=p.pk)

@login_required
def project_detail(request, pk):
    project = _project(request, pk)
    tasks = list(project.tasks.select_related("assignee").annotate(n_comments=Count("comments")))
    codes = [c for c, _ in STATUSES]
    cols = []
    for i, (code, label) in enumerate(STATUSES):
        col = [t for t in tasks if t.status == code]
        for t in col:
            t.prev = codes[i - 1] if i > 0 else None
            t.next = codes[i + 1] if i < len(codes) - 1 else None
        cols.append({"label": label, "tasks": col})
    return render(request, "project.html", {"project": project, "columns": cols, "members": project.members.all()})

@require_POST
@login_required
def member_add(request, pk):
    project = _project(request, pk)
    user = User.objects.filter(username=request.POST.get("username", "").strip()).first()
    if not user: messages.error(request, "No user with that username.")
    elif project.members.filter(pk=user.pk).exists(): messages.error(request, "Already a member.")
    else:
        project.members.add(user)
        notify(user, f"{request.user.username} added you to “{project.name}”", f"/projects/{project.pk}/")
        broadcast(project.pk)
    return redirect("project_detail", pk=pk)

@require_POST
@login_required
def task_create(request, pk):
    project = _project(request, pk)
    title = request.POST.get("title", "").strip()
    if title:
        who = _assignee(project, request.POST.get("assignee"))
        t = Task.objects.create(project=project, title=title, assignee=who, created_by=request.user)
        if who and who != request.user:
            notify(who, f"{request.user.username} assigned you “{t.title}”", f"/tasks/{t.pk}/")
        broadcast(project.pk)
    return redirect("project_detail", pk=pk)

@login_required
def task_detail(request, pk):
    t = _task(request, pk)
    return render(request, "task.html", {"task": t, "project": t.project, "members": t.project.members.all(),
        "comments": t.comments.select_related("author"), "statuses": STATUSES})

@require_POST
@login_required
def task_update(request, pk):
    t = _task(request, pk)
    if request.POST.get("status") in dict(STATUSES): t.status = request.POST["status"]
    if "assignee" in request.POST:
        who = _assignee(t.project, request.POST["assignee"])
        if who != t.assignee and who and who != request.user:
            notify(who, f"{request.user.username} assigned you “{t.title}”", f"/tasks/{t.pk}/")
        t.assignee = who
    t.save(); broadcast(t.project_id)
    return redirect("project_detail", pk=t.project_id) if request.POST.get("next") == "board" else redirect("task_detail", pk=pk)

@require_POST
@login_required
def comment_add(request, pk):
    t = _task(request, pk)
    text = request.POST.get("text", "").strip()
    if text:
        Comment.objects.create(task=t, author=request.user, text=text)
        for u in {t.assignee, t.created_by} - {None, request.user}:
            notify(u, f"{request.user.username} commented on “{t.title}”", f"/tasks/{t.pk}/")
        broadcast(t.project_id)
    return redirect("task_detail", pk=pk)

@login_required
def notifications(request):
    items = list(request.user.notifications.all()[:50])
    request.user.notifications.filter(read=False).update(read=True)
    return render(request, "notifications.html", {"items": items})

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save()); return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})
