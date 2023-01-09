from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.TaskList.as_view(), name="tasks_index"),
    path("tasks/<int:pk>/", views.TaskDetail.as_view(), name="detail"),
    path("tasks/create/", views.TaskCreate.as_view(), name="task_create"),
    path("tasks/<int:pk>/delete/", views.TaskDelete.as_view(), name="task_delete"),
    path("tasks/<int:pk>/update/", views.TaskUpdate.as_view(), name="task_update"),
    path("accounts/sign_up/", views.sign_up, name="sign_up"),
    path("accounts/profile/", views.user_profile_page, name="user_profile"),
    path("change_password/", views.UpdatePassword.as_view(), name="update_password"),
    path("password_edit_success/", views.password_edit_success, name="password_edit_success"),
]
