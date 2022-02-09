from contextlib import nullcontext
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import CreateEducatorCourseSerializer, StudentSerializer, EducatorSerializer, CourseSerializer, AssignmentSerializer, StudentAssignmentSerializer, EducatorCourseSerializer, StudentCourseSerializer
from .serializers import CreateStudentCourseSerializer, CreateStudentAssignmentSerializer
from .models import Student, Educator, Course, Assignment, StudentAssignment, StudentCourse, EducatorCourse
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student(request, user_id):
    try:
        student = Student.objects.get(user_id=user_id)
        serializer = StudentSerializer(student, many=False)
        return Response(serializer.data)
    except:
        print('Please create profile')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_educator(request, user_id):
    try:
        educator = Educator.objects.get(user_id=user_id)
        serializer = EducatorSerializer(educator, many=False)
        return Response(serializer.data)
    except:
        print('Please create profile')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_educator(request):
    serializer = EducatorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#both features
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

#educator features
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assignments_educator(request, educator_id):
    educator_courses = EducatorCourse.objects.filter(educator_id=educator_id)
    educator_course_list = list(educator_courses)
    educator_course_id_list = []
    for course in educator_course_list:
        educator_course_id_list.append(course.course_id)

    
    assignments = Assignment.objects.filter(assignment_course_id__in=educator_course_id_list).order_by('assignment_due_date')
    serializer = AssignmentSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_courses_educator(request, educator_id):
    educator_courses = EducatorCourse.objects.filter(educator_id=educator_id)
    serializer = EducatorCourseSerializer(educator_courses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def oversee_class(request):
    serializer = CreateEducatorCourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_class(request, educator_id, course_id):
    course = EducatorCourse.objects.filter(educator_id=educator_id, course_id=course_id )
    serializer = EducatorCourseSerializer(course, many=False)
    course.delete()
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_assignment(request, course_id):
    assignment_serializer = AssignmentSerializer(data=request.data)
    if assignment_serializer.is_valid():
        assignment_serializer.save()
        #after created adds to course assignments
        # course_data = {
        #     "course": course_id,
        #     "assignment": assignment_serializer.instance.id
        # }
        
        # serializer = CreateCourseAssignmentSerializer(data=course_data)
        # if serializer.is_valid():
        #     serializer.save()
        return Response(assignment_serializer.data, status=status.HTTP_201_CREATED)
    return Response(assignment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    serializer = AssignmentSerializer(assignment, many=False)
    assignment.delete()
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    serializer = AssignmentSerializer(assignment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    
#student features
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_class(request):
    serializer = CreateStudentCourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unregister_class(request, student_id, course_id):
    course = StudentCourse.objects.filter(student_id=student_id, course_id=course_id )
    serializer = StudentCourseSerializer(course, many=False)
    course.delete()
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_courses(request, student_id):
    student_courses = StudentCourse.objects.filter(student_id=student_id)
    serializer = StudentCourseSerializer(student_courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assignments_one_course(request, course_id):
    assignments = Assignment.objects.filter(assignment_course_id=course_id)
    serializer = AssignmentSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assignments(request, student_id):
    student_courses = StudentCourse.objects.filter(student_id=student_id)
    student_course_list = list(student_courses)
    student_course_id_list = []
    for course in student_course_list:
        student_course_id_list.append(course.course_id)

    
    assignments = Assignment.objects.filter(assignment_course_id__in=student_course_id_list).order_by('assignment_due_date')
    serializer = AssignmentSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assignment_status(request, student_id):
    student_status = StudentAssignment.objects.filter(student_id=student_id)
    serializer = StudentAssignmentSerializer(student_status, many=True)
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