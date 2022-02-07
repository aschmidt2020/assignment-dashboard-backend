from dataclasses import field
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student, Educator, Course, Assignment, StudentAssignment, StudentCourse, EducatorCourse, CourseAssignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

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
    class Meta:
        model = Assignment
        fields = '__all__'

class StudentAssignmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)
    assignment = AssignmentSerializer(many=False, read_only=True)
    
    class Meta:
        model: StudentAssignment
        fields = '__all__'
        
class StudentCourseSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)
    course = CourseSerializer(many=False, read_only=True)
    
    class Meta:
        model: StudentCourse
        fields = '__all__'

class EducatorCourseSerializer(serializers.ModelSerializer):
    educator = EducatorSerializer(many=False, read_only=True)
    course = CourseSerializer(many=False, read_only=True)
    
    class Meta:
        model: EducatorCourse
        fields = '__all__'

class CourseAssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False, read_only=True)
    assignment = AssignmentSerializer(many=False, read_only=True)
    
    class Meta:
        model: CourseAssignment
        fields = '__all__'