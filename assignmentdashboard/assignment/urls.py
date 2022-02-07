from django.urls import path
from assignment import views

urlpatterns = [
    path('user/<int:user_id>/', views.get_user),
    path('student/registerclass/', views.register_class),
    path('student/getcourses/<int:student_id>/', views.get_courses),
    path('student/getassignments/<int:student_id>/', views.get_assignments),
    path('student/updateassignmentstatus/<int:assignment_id>/', views.update_assignment_status)
]
