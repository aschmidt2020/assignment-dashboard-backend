from django.contrib import admin
from .models import Student, Educator, Course, Assignment, StudentAssignment, StudentCourse, EducatorCourse
admin.site.register(Student)
admin.site.register(Educator)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(StudentAssignment)
admin.site.register(StudentCourse)
admin.site.register(EducatorCourse)
