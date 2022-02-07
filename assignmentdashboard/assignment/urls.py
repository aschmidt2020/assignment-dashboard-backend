from django.urls import path
from assignment import views

urlpatterns = [
    path('user/<int:user_id>/', views.get_user),
    path('student/<int:user_id>/', views.get_student),
    path('educator/<int:user_id>/', views.get_educator),
    path('student/registerclass/', views.register_class),
    path('student/unregisterclass/<int:student_id>/<int:course_id>/', views.unregister_class),
    path('student/getcourses/<int:student_id>/', views.get_courses),
    path('student/getassignments/course/<int:course_id>/', views.get_assignments_one_course),
    path('student/getassignments/<int:student_id>/', views.get_assignments),
    path('student/updateassignmentstatus/<int:assignment_id>/', views.update_assignment_status),
    path('educator/addclass/', views.oversee_class),
    path('educator/removeclass/<int:educator_id>/<int:course_id>/', views.remove_class),
    path('educator/addassignment/<int:course_id>/', views.add_assignment),
    path('educator/deleteassignment/<int:assignment_id>/', views.delete_assignment),
    path('educator/updateassignment/<int:assignment_id>/', views.update_assignment),
    
]
