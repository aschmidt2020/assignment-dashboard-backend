from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# single models
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,  default=None)
    school_id = models.IntegerField(default=0)
    notepad_text = models.TextField(default=None, null=True)
    
    def __str__(self):
        return str(self.user.id)

class Educator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,  default=None)
    employee_id = models.IntegerField(default=0)
    notepad_text = models.TextField(default=None, null=True)
    
    def __str__(self):
        return str(self.user.id)

class Course(models.Model):
    course_school_id = models.CharField(max_length=50,  default=None)
    course_name = models.CharField(max_length=50,  default=None)
    course_credits = models.IntegerField(default=0)
    number_of_students = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.course_name)

class Assignment(models.Model):
    assignment_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, default=None)
    assignment_name = models.CharField(max_length=50,  default=None)
    assignment_desc = models.TextField(default=None)
    assignment_due_date = models.DateField(max_length=50,  default=None)
    assignment_instructions = models.TextField(default=None)
    students_viewed = models.IntegerField(default=0)
    students_in_progress = models.IntegerField(default=0)
    students_completed = models.IntegerField(default=0)
    assignment_link = models.TextField(default=None, null=True, blank=True)
    
    def __str__(self):
        return str(self.assignment_name)

#junction tables
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False,  default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False,  default=None)
    
    def __str__(self):
        return str(self.student.user.id) + str(self.course.course_name)

class EducatorCourse(models.Model):
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE,  null=False,  default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,  null=False,  default=None)

    def __str__(self):
        return str(self.educator.user.id) + str(self.course.course_name)
    
class StudentAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,  null=False,  default=None)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,  null=False,  default=None)
    assignment_prev_status = models.CharField(max_length=50,  default="Not Started")
    assignment_status = models.CharField(max_length=50,  default=None)
    
    def __str__(self):
        return str(self.assignment.assignment_name) + str(self.student.user.id)