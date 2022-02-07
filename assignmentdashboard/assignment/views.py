from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import StudentSerializer, EducatorSerializer, CourseSerializer, AssignmentSerializer, StudentAssignmentSerializer, EducatorCourseSerializer, StudentCourseSerializer, CourseAssignmentSerializer
from .serializers import CreateStudentCourseSerializer, CreateStudentAssignmentSerializer
from .models import Student, Educator, Course, Assignment, StudentAssignment, StudentCourse, EducatorCourse, CourseAssignment
from django.contrib.auth.models import User
from .serializers import UserSerializer

# Create your views here.
#get user info on login
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

#student features
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_class(request):
    serializer = CreateStudentCourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_courses(request, student_id):
    student_courses = StudentCourse.objects.filter(student_id=student_id)
    serializer = StudentCourseSerializer(student_courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assignments_one_course(request, course_id):
    assignments = CourseAssignment.objects.filter(course_id=course_id)
    serializer = CourseAssignmentSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assignments(request, student_id):
    student_courses = StudentCourse.objects.filter(student_id=student_id)
    student_course_list = list(student_courses)
    student_course_id_list = []
    for course in student_course_list:
        student_course_id_list.append(course.course_id)

    
    assignments = CourseAssignment.objects.filter(course_id__in=student_course_id_list)
    serializer = CourseAssignmentSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_assignment_status(request, assignment_id):
    try:
        assignment = StudentAssignment.objects.get(assignment_id=assignment_id)
        serializer = StudentAssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        serializer = CreateStudentAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)