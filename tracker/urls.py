from django.contrib.auth import views as auth
from django.urls import path
from . import views as v
urlpatterns = [
    path("", v.dashboard, name="dashboard"),
    path("projects/new/", v.project_create, name="project_create"),
    path("projects/<int:pk>/", v.project_detail, name="project_detail"),
    path("projects/<int:pk>/members/", v.member_add, name="member_add"),
    path("projects/<int:pk>/tasks/new/", v.task_create, name="task_create"),
    path("tasks/<int:pk>/", v.task_detail, name="task_detail"),
    path("tasks/<int:pk>/update/", v.task_update, name="task_update"),
    path("tasks/<int:pk>/comment/", v.comment_add, name="comment_add"),
    path("notifications/", v.notifications, name="notifications"),
    path("register/", v.register, name="register"),
    path("login/", auth.LoginView.as_view(), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
]
