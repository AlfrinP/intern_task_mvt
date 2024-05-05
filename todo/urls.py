from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signin/", views.signin, name="signin"),
    path("register/", views.register, name="register"),
    path("signout/", views.signout, name="signout"),
    path("mark_as_done/<int:task_id>/", views.mark_as_done, name="mark_as_done"),
    path("mark_as_undone/<int:task_id>/",views.mark_as_undone, name="mark_as_undone"),
    path("create_task/", views.createTask, name="create_task"),
    path("update_task/<int:task_id>/", views.updateTask, name="update_task"),
    path("delete_task/<int:task_id>/", views.deleteTask, name="delete_task"),
]
