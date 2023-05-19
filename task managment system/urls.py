from django.urls import path
from .views import task_list, create_task, update_task, delete_task, register_user, logout

urlpatterns = [
    path('task/list/', task_list, name='task_list'),
    path('task/create/', create_task, name='create_task'),
    path('task/update/<int:task_id>/', update_task, name='update_task'),
    path('task/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('register/', register_user, name='register_user'),
    path('logout/', logout, name='logout'),
]
