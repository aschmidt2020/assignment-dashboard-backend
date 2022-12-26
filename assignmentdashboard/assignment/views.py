from contextlib import nullcontext
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import CreateEducatorCourseSerializer, StudentSerializer, EducatorSerializer, CourseSerializer, AssignmentSerializer, StudentAssignmentSerializer, EducatorCourseSerializer, StudentCourseSerializer
from .serializers import CreateAssignmentSerializer, CreateStudentCourseSerializer, CreateStudentAssignmentSerializer, StudentAssignmentAndStatusSerializer
from .models import Student, Educator, Course, Assignment, StudentAssignment, StudentCourse, EducatorCourse
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.db.models import Count, Prefetch
from datetime import date, datetime, timedelta

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
        return Response('Please finish creating profile.', status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_educator(request, user_id):
    try:
        educator = Educator.objects.get(user_id=user_id)
        serializer = EducatorSerializer(educator, many=False)
        return Response(serializer.data)
    except:
         return Response('Please finish creating profile.', status=204)

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

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def save_notes(request, user_id):
    try:
        educator = Educator.objects.get(user_id=user_id) #ensures user is on educator table
        serializer = EducatorSerializer(educator, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        student = Student.objects.get(user_id=user_id)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
def get_assignment_status_educator(request, educator_id):
    educator_courses = EducatorCourse.objects.filter(educator_id=educator_id)
    educator_course_list = list(educator_courses)
    educator_course_id_list = []
    for course in educator_course_list:
        educator_course_id_list.append(course.course_id)
    
    today = date.today()
    last_three = date.today() - timedelta(days=3)
    next_three = date.today() + timedelta(days=3)
    next_seven = date.today() + timedelta(days=7)

    assignments = Assignment.objects.filter(assignment_course_id__in=educator_course_id_list).filter(assignment_archived=False)
    assignments_next_three = assignments.filter(assignment_due_date__gte = today).filter(assignment_due_date__lt = next_three)
    assignments_next_seven = assignments.filter(assignment_due_date__gte=next_three).filter(assignment_due_date__lt=next_seven)
    assignments_later = assignments.filter(assignment_due_date__gte=next_seven)
    assignments_completed = assignments.filter(assignment_due_date__lt=today).filter(assignment_due_date__gte=last_three)
    assignments_archived = Assignment.objects.filter(assignment_course_id__in=educator_course_id_list).filter(assignment_archived=True)

    serializer = {
        'next_three': AssignmentSerializer(assignments_next_three, many=True).data,
        'next_seven': AssignmentSerializer(assignments_next_seven, many=True).data,
        'later': AssignmentSerializer(assignments_later, many=True).data,
        'completed': AssignmentSerializer(assignments_completed, many=True).data,
        'archived': AssignmentSerializer(assignments_archived, many=True).data
    }
    return Response(serializer)

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
    assignment_serializer = CreateAssignmentSerializer(data=request.data)
    if assignment_serializer.is_valid():
        assignment_serializer.save()
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
        
        #update course info
        course = Course.objects.get(id=request.data['course'])
        course.number_of_students = len(StudentCourse.objects.filter(course_id=course.id))
        course.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unregister_class(request, student_id, course_id):
    course = StudentCourse.objects.filter(student_id=student_id, course_id=course_id )
    serializer = StudentCourseSerializer(course, many=False)
    course.delete()
    
    #update course info
    course_updated = Course.objects.get(id=course_id)
    course_updated.number_of_students = len(StudentCourse.objects.filter(course_id=course_updated.id))
    course_updated.save()
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
    student_courses = list(StudentCourse.objects.filter(student_id=student_id))
    student_course_id_list = []
    for course in student_courses:
        student_course_id_list.append(course.course_id)

    assignments = Assignment.objects.filter(assignment_course_id__in=student_course_id_list).order_by('assignment_due_date')
    serializer = AssignmentSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assignment_status(request, student_id):
    student_courses = list(StudentCourse.objects.filter(student_id=student_id))
    student_course_id_list = []
    for course in student_courses:
        student_course_id_list.append(course.course_id)

    if len(student_course_id_list) > 0:
        assignments = query_student_assignments_status(student_course_id_list, student_id)
        return Response(assignments)
    else:
        return Response({'overdue': [], 'next_three': [], 'next_seven': [], 'later': [], 'completed': []})

def query_student_assignments_status(student_course_list, student_id):
    today = date.today()
    last_three = date.today() - timedelta(days=3)
    next_three = date.today() + timedelta(days=3)
    next_seven = date.today() + timedelta(days=7)
    student_course_list_tuple = ''

    if len(student_course_list) == 1:
        student_course_list_tuple = f'({student_course_list[0]})'
    else:
        student_course_list_tuple = str(tuple(student_course_list))

    assignments_overdue = Assignment.objects.raw(f'''SELECT * FROM assignment_assignment a
                                                    LEFT JOIN (
                                                        SELECT * FROM assignment_studentassignment sa1
                                                        WHERE sa1.student_id={student_id}
                                                        ) sa2
                                                    ON a.id = sa2.assignment_id
                                                    WHERE a.assignment_course_id in {student_course_list_tuple}
                                                    and (sa2.assignment_status NOT LIKE 'Completed' or sa2.assignment_status is null)
                                                    and a.assignment_due_date < '{today}'
                                                    and a.assignment_archived = false
                                                    ''')

    assignments_next_three = Assignment.objects.raw(f'''SELECT * FROM assignment_assignment a
                                                        LEFT JOIN (
                                                            SELECT * FROM assignment_studentassignment sa1
                                                            WHERE sa1.student_id={student_id}
                                                            ) sa2
                                                        ON a.id = sa2.assignment_id
                                                        WHERE a.assignment_course_id in {student_course_list_tuple}
                                                        and (sa2.assignment_status NOT LIKE 'Completed' or sa2.assignment_status is null)
                                                        and a.assignment_due_date BETWEEN '{today}' and '{next_three}'
                                                        ''')     

    assignments_next_seven = Assignment.objects.raw(f'''SELECT * FROM assignment_assignment a
                                                        LEFT JOIN (
                                                            SELECT * FROM assignment_studentassignment sa1
                                                            WHERE sa1.student_id={student_id}
                                                            ) sa2
                                                        ON a.id = sa2.assignment_id
                                                        WHERE a.assignment_course_id in {student_course_list_tuple}
                                                        and (sa2.assignment_status NOT LIKE 'Completed' or sa2.assignment_status is null)
                                                        and a.assignment_due_date BETWEEN '{next_three}' and '{next_seven}'
                                                        ''')     

    assignments_completed = Assignment.objects.raw(f'''SELECT * FROM assignment_assignment a
                                                        LEFT JOIN (
                                                            SELECT * FROM assignment_studentassignment sa1
                                                            WHERE sa1.student_id={student_id}
                                                            ) sa2
                                                        ON a.id = sa2.assignment_id
                                                        WHERE a.assignment_course_id in {student_course_list_tuple}
                                                        and sa2.assignment_status LIKE 'Completed'
                                                        and a.assignment_due_date BETWEEN '{last_three}' and '{next_three}'
                                                        and a.assignment_archived = false
                                                        ''')       

    assignments_later = Assignment.objects.raw(f'''SELECT * FROM assignment_assignment a
                                                        LEFT JOIN (
                                                            SELECT * FROM assignment_studentassignment sa1
                                                            WHERE sa1.student_id={student_id}
                                                            ) sa2
                                                        ON a.id = sa2.assignment_id
                                                        WHERE a.assignment_course_id in {student_course_list_tuple}
                                                        and (sa2.assignment_status NOT LIKE 'Completed' or sa2.assignment_status is null)
                                                        and a.assignment_due_date >= '{next_seven}'
                                                        ''')      

    assignments_archived = Assignment.objects.raw(f'''SELECT * FROM assignment_assignment a
                                                        LEFT JOIN(
                                                            SELECT * FROM assignment_studentassignment sa1
                                                            where sa1.student_id={student_id}
                                                            ) sa2
                                                        ON a.id = sa2.assignment_id
                                                        WHERE a.assignment_course_id in {student_course_list_tuple}
                                                        and a.assignment_archived=true''')

    serializer = {'overdue': StudentAssignmentAndStatusSerializer(assignments_overdue, many=True).data,
        'next_three': StudentAssignmentAndStatusSerializer(assignments_next_three, many=True).data,
        'next_seven': StudentAssignmentAndStatusSerializer(assignments_next_seven, many=True).data,
        'later': StudentAssignmentAndStatusSerializer(assignments_later, many=True).data,
        'completed': StudentAssignmentAndStatusSerializer(assignments_completed, many=True).data,
        'archived': StudentAssignmentAndStatusSerializer(assignments_archived, many=True).data
        }

    return serializer

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_assignment_status(request, student_id, assignment_id):
    try:
        assignment = StudentAssignment.objects.get(student_id=student_id, assignment_id=assignment_id)
        serializer = StudentAssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            #update assignment 
            assignment = Assignment.objects.get(id=assignment_id)
            if request.data['assignment_status'] == 'Viewed':
                assignment.students_viewed = assignment.students_viewed + 1
            elif request.data['assignment_status'] == 'In Progress':
                assignment.students_in_progress = assignment.students_in_progress + 1
            elif request.data['assignment_status'] == 'Completed':
                assignment.students_completed = assignment.students_completed + 1
            
            if request.data['assignment_prev_status'] == 'Viewed':
                assignment.students_viewed = assignment.students_viewed - 1
            elif request.data['assignment_prev_status'] == 'In Progress':
                assignment.students_in_progress = assignment.students_in_progress - 1
            elif request.data['assignment_prev_status'] == 'Completed':
                assignment.students_completed = assignment.students_completed - 1
            
            assignment.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        serializer = CreateStudentAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            #update assignment 
            assignment = Assignment.objects.get(id=assignment_id)
            if request.data['assignment_status'] == 'Viewed':
                assignment.students_viewed = assignment.students_viewed + 1
            elif request.data['assignment_status'] == 'In Progress':
                assignment.students_in_progress = assignment.students_in_progress + 1
            elif request.data['assignment_status'] == 'Completed':
                assignment.students_completed = assignment.students_completed + 1
            assignment.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)