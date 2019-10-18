from django.urls import path
from .views.viewsTask import *
from .views.viewsUser import *

urlpatterns = [
    path('', home, name='home'),
    path('create/', createTask, name='createTask'),
    path('list/', listTask, name='listTask'),
    path('update/<int:id>', updateTask, name='updateTask'),
    path('remove/<int:id>', removeTask, name='removeTask'),
    path('createUser/', createUser, name='createUser'),
    path('login/', loginUser, name='loginUser'),
    path('logout/', logoutUser, name='logoutUser'),
]