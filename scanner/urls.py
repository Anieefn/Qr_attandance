from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/<int:userid>/<int:year>/', views.teacher, name='home'),
    path('attendance/<int:userid>/', views.attendance, name='attendance'),
    path('student/<int:userid>/', views.student_dashboard, name='student'),
    path('report/<int:userid>/', views.report, name='report'),
    path('logout/', views.logout, name='logout'),
    path('update_student/<int:userid>/', views.update_student, name='update_student'),
    path('delete_student/<int:userid>/<int:student_id>/', views.delete_student, name='delete_student'),
]
