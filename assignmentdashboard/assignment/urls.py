from django.urls import path
from assignment import views

urlpatterns = [
    path('user/user_id/<int:user_id>/', views.get_user),
    path('student/user_id/<int:user_id>/', views.get_student),
    path('educator/user_id/<int:user_id>/', views.get_educator),
    path('student/register/', views.register_student),
    path('educator/register/', views.register_educator),
    path('getcourses/', views.get_all_courses),
    path('student/registerclass/', views.register_class),
    path('student/unregisterclass/student_id/<int:student_id>/course_id/<int:course_id>/', views.unregister_class),
    path('student/getcourses/student_id/<int:student_id>/', views.get_courses),
    path('student/getassignmentstatus/student_id/<int:student_id>/', views.get_assignment_status),
    path('getassignments/course/course_id/<int:course_id>/', views.get_assignments_one_course),
    path('student/getassignments/student_id/<int:student_id>/', views.get_assignments),
    path('student/updateassignmentstatus/student_id/<int:student_id>/assignment_id/<int:assignment_id>/', views.update_assignment_status),
    path('educator/getcourses/educator_id/<int:educator_id>/', views.get_courses_educator),
    path('educator/getassignments/educator_id/<int:educator_id>/', views.get_assignments_educator),
    path('educator/getassignmentstatus/',views.get_assignment_status_educator),
    path('educator/addclass/', views.oversee_class),
    path('educator/removeclass/educator_id/<int:educator_id>/course_id/<int:course_id>/', views.remove_class),
    path('educator/addassignment/course_id/<int:course_id>/', views.add_assignment),
    path('educator/deleteassignment/assignment_id/<int:assignment_id>/', views.delete_assignment),
    path('educator/updateassignment/assignment_id/<int:assignment_id>/', views.update_assignment),
    
]
