from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
from geniotechapp.custom_decorator import custom_staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Course
from .forms import CustomUserCreationForm, CourseForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Instructor, TimeSlot, Course, TimeSlotAssignment
from .forms import TimeSlotAssignmentForm

from django.contrib.auth import logout
from django.shortcuts import render, redirect


def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})
    

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')  # Replace 'login' with the name of your login URL pattern


class CustomUserRegistrationView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'Registration.html'
    success_url = reverse_lazy('login')  # Redirect to the login page after successful registration

from django.contrib.auth.views import LoginView

class CustomUserLoginView(LoginView):
    template_name = 'login.html'  # Customize the login template


@login_required
@custom_staff_member_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            
            # Check if a course with the same title already exists
            if Course.objects.filter(title=title).exists():
                form.add_error('title', 'A course with this title already exists.')
            else:
                course = form.save()
                course_ids = ",".join(str(course.course_id) for course in Course.objects.all())
                Instructor.objects.all().update(course_taught=course_ids)
                return redirect('course_list')
    else:
        form = CourseForm()
    
    return render(request, 'course_form.html', {'form': form})

@login_required
@custom_staff_member_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form, 'course': course})

from django.shortcuts import render, redirect
from django.http import HttpResponse
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    instructors = Instructor.objects.all()

    if request.method == 'POST':
        
        student_id = request.user.id
        instructor_id = request.POST.get('instructor_id')
        time_slot_assignment = get_object_or_404(TimeSlotAssignment, id=request.POST.get('timeslot_id'))
        timeslot_id = time_slot_assignment.timeslot_id
        if instructor_id:
            # Get the selected instructor
            selected_instructor = get_object_or_404(Instructor, pk=instructor_id)
            time_slot = get_object_or_404(TimeSlot, pk=timeslot_id)

            # Retrieve the existing JSON data
            enrolled_students = course.enrolled_students or {}

            # Check if the student is already enrolled with an instructor for this course
            if str(student_id) not in enrolled_students:
                # If not, create a new entry for the student for this course
                enrolled_students[student_id] = {str(course_id): {str(instructor_id): str(timeslot_id)}}

                # Save the updated JSON data
                course.enrolled_students = enrolled_students
                course.save()

                # Update the instructor's students_taught field
                students_taught = selected_instructor.students_taught or {}
                if str(student_id) in students_taught:
                    students_taught[str(student_id)].append({str(course_id): str(timeslot_id)})
                else:
                    students_taught[str(student_id)] = [{str(course_id): str(timeslot_id)}]
                selected_instructor.students_taught = students_taught
                selected_instructor.save()


                time_slot_assignment = get_object_or_404(TimeSlotAssignment, timeslot_id=timeslot_id)
                print(time_slot_assignment)
                zoom_link = time_slot_assignment.zoom_link

                # Send the Zoom link email to the student
                print(request.user.email)
                send_zoom_link_email(student_email=request.user.email, instructor=selected_instructor.full_name, time_slot=time_slot, course=course, zoom_link=zoom_link)
            else:
                time_slot_assignment = get_object_or_404(TimeSlotAssignment, timeslot_id=timeslot_id)
                print(time_slot_assignment)
                return HttpResponse("You are already enrolled in this course.", content_type="text/plain")


            return redirect('course_details', course_id=course_id)
    course = get_object_or_404(Course, pk=course_id)
    enrolled_students = course.enrolled_students or {}
    if(request.user.is_instructor == 1):
        list_of_students = {}
        for each in enrolled_students:
            student = get_object_or_404(CustomUser, pk=each)
            further_detail = enrolled_students[str(student.id)][str(course_id)]
            enrolled_time_slot = further_detail[str(request.user.id)]
            enrolled_time = get_object_or_404(TimeSlot, pk=enrolled_time_slot)
            enrolled_time = "On " + str(enrolled_time.day) + " from " +  str(enrolled_time.start_time) + " To " +  str(enrolled_time.end_time)
            detail_of_student = {}
            detail_of_student[student.full_name] = enrolled_time
            list_of_students[student.id] = detail_of_student
        
        print(list_of_students)
            
        return render(request, 'instructor_course_details.html', {'course': course, 'list_of_students': list_of_students})
    elif(request.user.is_admin == 1):
        course = get_object_or_404(Course, pk=course_id)
        time_slot_assignments = TimeSlotAssignment.objects.filter(course=course)

        for assignment in time_slot_assignments:
            # Check if a Zoom link is already created for the assignment
            if assignment.zoom_link:
                assignment.zoom_link_created = True
            else:
                assignment.zoom_link_created = False

        context = {
            'course': course,
            'time_slot_assignments': time_slot_assignments,
        }

        return render(request, 'course_time_slots.html', context)
    else:
        
        student_id = request.user.id

        instructors = Instructor.objects.all()
        time_slots = TimeSlotAssignment.objects.filter(course_id=course_id)

        if str(student_id) in enrolled_students:
            
            further_detail = enrolled_students[str(student_id)][str(course_id)]
            enrolled_instructor_id = list(further_detail.keys())[0]
            enrolled_time_slot = further_detail[enrolled_instructor_id]
            
            enrolled_instructor = get_object_or_404(Instructor, pk=enrolled_instructor_id)
            enrolled_time = get_object_or_404(TimeSlot, pk=enrolled_time_slot)
            enrolled_time = "On " + str(enrolled_time.day) + " from " +  str(enrolled_time.start_time) + " To " +  str(enrolled_time.end_time)

            enrollment_status = "You are already enrolled in this course with instructor " + str(enrolled_instructor.full_name) + " " + enrolled_time
            return render(request, 'course_details.html', {'course': course,  'enrollment_status': enrollment_status})
        else:
            # Create a dictionary to store available options
            available_options = {}
            for instructor in instructors:
                # Get time slots assigned to the instructor for this course
                assigned_time_slots = time_slots.filter(instructor_id=instructor.customuser_ptr_id)

            print(assigned_time_slots)
            if assigned_time_slots:
                available_options[instructor] = assigned_time_slots
        # ... existing code ...
        
            return render(request, 'course_details.html', {'course': course, 'instructors': instructors, 'available_options': available_options})
    
    
from django.core.mail import send_mail

from django.core.mail import EmailMessage, get_connection
from django.conf import settings



def send_zoom_link_email(student_email, instructor, time_slot, course, zoom_link):

    subject = f"Zoom Link for {course.title} - {instructor}"
    message = f"Dear student,\n\nYou have successfully enrolled in the course {course.title}.\n\nInstructor: {instructor}\nTime Slot: {time_slot.day} {time_slot.start_time} - {time_slot.end_time}\nZoom Link: {zoom_link}\n\nBest regards,\nYour Website Team"
    from_email = "pathikp901@gmail.com"  # Change this to your email address
    recipient_list = [student_email]

    with get_connection(  
           host=settings.EMAIL_HOST, 
     port=settings.EMAIL_PORT,  
     username=settings.EMAIL_HOST_USER, 
     password=settings.EMAIL_HOST_PASSWORD, 
     use_tls=settings.EMAIL_USE_TLS  
       ) as connection:  
           subject = subject  
           email_from = settings.EMAIL_HOST_USER  
           recipient_list = [student_email]  
           message = message
           EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()  
    # send_mail(subject, message, from_email, recipient_list)
    
@login_required
@custom_staff_member_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'course_confirm_delete.html', {'course': course})

@login_required
def course_list(request, age_range):
    user = request.user
    if age_range == '6-9':
        courses = Course.objects.filter(from_age__gte=6, to_age__lte=9)
    elif age_range == '10-17':
        courses = Course.objects.filter(from_age__gte=10, to_age__lte=17)
    else:
        # Handle other cases if needed
        courses = Course.objects.all()

    return render(request, 'course_list.html', {'is_admin': user.is_admin, 'courses': courses})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Instructor
from .forms import InstructorForm


from django.shortcuts import render, redirect


# ...
def instructor_list(request):
    instructors = Instructor.objects.all()
    return render(request, 'instructor_list.html', {'instructors': instructors})

from django.shortcuts import render, redirect
from .forms import InstructorForm  # Import the custom form

@custom_staff_member_required
def instructor_registration(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            # form.save()
            instructor = form.save()

            # Fetch all courses and concatenate their IDs into a comma-separated string
            course_ids = ",".join(str(course.course_id) for course in Course.objects.all())

            # Update the course_taught field
            instructor.course_taught = course_ids
            instructor.set_password(request.POST['password'])
            instructor.save()
            return redirect('instructor_list')
        else:
            print("Form is invalid. Errors:", form.errors)
    else:
        form = InstructorForm()
    return render(request, 'instructor_form.html', {'form': form})


@custom_staff_member_required
def edit_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    if request.method == 'POST':
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect('instructor_list')
    else:
        form = InstructorForm(instance=instructor)
    return render(request, 'instructor_form.html', {'form': form, 'instructor': instructor})

@custom_staff_member_required
def delete_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    if request.method == 'POST':
        instructor.delete()
        return redirect('instructor_list')
    return render(request, 'instructor_confirm_delete.html', {'instructor': instructor})

from django.shortcuts import render, redirect
from .models import TimeSlot
from .forms import TimeSlotForm

def create_time_slot(request):
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_time_slot')  # Redirect to a view that lists all time slots
    else:
        form = TimeSlotForm()
    
    return render(request, 'create_time_slot.html', {'form': form})


# def assign_time_slot(request, instructor_id):
#     instructor = Instructor.objects.get(pk=instructor_id)
#     available_time_slots = TimeSlot.objects.filter(is_available=True)
#     assigned_slots = TimeSlotAssignment.objects.filter(instructor=instructor)

#     if request.method == 'POST':
#         form = TimeSlotAssignmentForm(request.POST)
#         if form.is_valid():
#             course = form.cleaned_data['course']
#             timeslot = form.cleaned_data['timeslot']

#             if timeslot.is_available:
#                 TimeSlotAssignment.objects.create(
#                     instructor=instructor,
#                     course=course,
#                     timeslot=timeslot,
#                 )

#                 timeslot.is_available = False
#                 timeslot.save()

#             return redirect('instructos/6/assign-time-slot', instructor_id=instructor_id)

#     else:
#         form = TimeSlotAssignmentForm()

#     return render(request, 'assign_time_slot.html', {
#         'instructor': instructor,
#         'available_time_slots': available_time_slots,
#         'assigned_slots': assigned_slots,
#         'form': form,
#     })

from .models import TimeSlotAssignment  # Import the new model

def assign_time_slot(request, instructor_id):
    instructor = Instructor.objects.get(pk=instructor_id)
    # available_time_slots = TimeSlot.objects.filter()
    # assigned_slots = TimeSlotAssignment.objects.filter(instructor=instructor)

    assigned_slots = TimeSlotAssignment.objects.filter(instructor_id=instructor_id)
    assigned_slot_ids = [assignment.timeslot.id for assignment in assigned_slots]
    
    available_time_slots = TimeSlot.objects.exclude(id__in=assigned_slot_ids)

    if request.method == 'POST':
        form = TimeSlotAssignmentForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            timeslot = form.cleaned_data['timeslot']

            # Check if the assignment already exists for this instructor and timeslot
            existing_assignment = assigned_slots.filter(timeslot=timeslot).first()

            if not existing_assignment:
                # If no assignment exists, create a new one for the instructor
                TimeSlotAssignment.objects.create(
                    instructor=instructor,
                    course=course,
                    timeslot=timeslot,
                )

            return redirect('/instructors/'+str(instructor_id)+'/assign-time-slot', instructor_id=instructor_id)

    else:
        form = TimeSlotAssignmentForm()

    return render(request, 'assign_time_slot.html', {
        'instructor': instructor,
        'available_time_slots': available_time_slots,
        'assigned_slots': assigned_slots,
        'form': form,
    })

def assign_zoom_link(request, assignment_id):
    time_slot_assignment = get_object_or_404(TimeSlotAssignment, pk=assignment_id)

    if request.method == 'POST':
        zoom_link = request.POST.get('zoom_link')
        if zoom_link:
            time_slot_assignment.zoom_link = zoom_link
            time_slot_assignment.save()
            return redirect('course_details', course_id=time_slot_assignment.course.course_id)
    print(time_slot_assignment)
    context = {
        'time_slot_assignment': time_slot_assignment,
    }

    return render(request, 'assign_zoom_link.html', context)
