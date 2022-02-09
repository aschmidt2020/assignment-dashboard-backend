from dataclasses import field, fields
from pickletools import read_floatnl
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student, Educator, Course, Assignment, StudentAssignment, StudentCourse, EducatorCourse

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Student
        fields = '__all__'
        
class EducatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Educator
        fields = '__all__'
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
             
class AssignmentSerializer(serializers.ModelSerializer):
    assignment_course = CourseSerializer(many=False, read_only=True)
    class Meta:
        model = Assignment
        fields = '__all__'


class CreateAssignmentSerializer(serializers.ModelSerializer):
    assignment_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Assignment
        fields = '__all__'

class StudentAssignmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)
    assignment = AssignmentSerializer(many=False, read_only=True)
    
    class Meta:
        model = StudentAssignment
        fields = '__all__'

class CreateStudentAssignmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    assignment = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all())
    
    class Meta:
        model = StudentAssignment
        fields = '__all__'
        
class StudentCourseSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)
    course = CourseSerializer(many=False, read_only=True)
    
    class Meta:
        model = StudentCourse
        fields = '__all__'

class CreateStudentCourseSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = StudentCourse
        fields = '__all__'
        
class EducatorCourseSerializer(serializers.ModelSerializer):
    educator = EducatorSerializer(many=False, read_only=True)
    course = CourseSerializer(many=False, read_only=True)
    
    class Meta:
        model = EducatorCourse
        fields = '__all__'

class CreateEducatorCourseSerializer(serializers.ModelSerializer):
    educator = serializers.PrimaryKeyRelatedField(queryset=Educator.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = EducatorCourse
        fields = '__all__'
# class CourseAssignmentSerializer(serializers.ModelSerializer):
#     course = CourseSerializer(many=False, read_only=True)
#     assignment = AssignmentSerializer(many=False, read_only=True)
    
#     class Meta:
#         model = CourseAssignment
#         fields = '__all__'

# class CreateCourseAssignmentSerializer(serializers.ModelSerializer):
#     assignment = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all())
#     course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
#     class Meta:
#         model = CourseAssignment
#         fields = '__all__'