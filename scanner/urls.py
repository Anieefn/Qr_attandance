from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/<int:userid>/', views.teacher, name='home'),
    path('attendance/<int:userid>/', views.attendance, name='attendance')
]
