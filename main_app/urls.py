from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('tasks/', views.TaskList.as_view(), name='tasks_index'),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='tasks_detail'),
    path('tasks/create/', views.TaskCreate.as_view(), name='tasks_create'),
]
