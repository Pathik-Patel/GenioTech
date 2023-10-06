from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InstructorRegistrationForm, ParentRegistrationForm, PasswordChangeForm, CustomUser
from django.core.exceptions import ObjectDoesNotExist

# Registration view
def register(request):
    if request.method == 'POST':
        form = None
        is_instructor = request.POST.get('is_instructor', False)
        if is_instructor:
            form = InstructorRegistrationForm(request.POST)
        else:
            form = ParentRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('register')  # Redirect to the dashboard after registration
    else:
        form = ParentRegistrationForm()  # Default to parent registration form

    return render(request, 'Registration.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after login
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html')

# Forget Password view
def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
            # Generate a password reset token, send it to the user's email, and handle password reset logic
            # This involves sending an email with a reset link or token as per your project's requirements.
            # You can use Django's built-in password reset views for this purpose.
        except ObjectDoesNotExist:
            messages.error(request, 'User with this email does not exist.')

    
    return render(request, 'registration/forget_password.html')

# Add Course view (assuming you have a CourseForm)
@login_required
def add_course(request):
    if request.method == 'POST':
        pass
        # Create a form to handle course data
        # Validate and save the course data
        
    return render(request, 'courses/add_course.html')

# Add Instructor view (assuming you have an InstructorForm)
@login_required
def add_instructor(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_instructor = True  # Set the user as an instructor
            user.save()
            # You can also create an Instructor instance with additional instructor-specific fields if needed.
            # instructor = Instructor(user=user, ...)
            # instructor.save()
            messages.success(request, 'Instructor added successfully.')
            return redirect('dashboard')
    else:
        form = CustomUserForm()

    return render(request, 'instructors/add_instructor.html', {'form': form})

# Dashboard view (protected by login_required decorator)
@login_required
def dashboard(request):
    # Logic for the dashboard view
    return render(request, 'dashboard.html')
