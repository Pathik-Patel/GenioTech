"""geniotech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from geniotechapp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('admin', admin.site.urls),
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('logout/',views.custom_logout, name='logout'),
    path('register', views.CustomUserRegistrationView.as_view(), name='register'),
    path('courses/<str:age_range>/', views.course_list, name='course_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('add_instructor/', views.instructor_registration, name='add_instructor'),
    path('course-details/<int:course_id>/', views.course_details, name='course_details'),
    path('course_enroll/<int:course_id>/', views.course_details, name='course_enroll'),
    path('edit_instructor/<int:instructor_id>/', views.edit_instructor, name='edit_instructor'),
    path('delete_instructor/<int:instructor_id>/', views.delete_instructor, name='delete_instructor'),
    path('instructor_list/', views.instructor_list, name='instructor_list'),
    path('create-time-slot/', views.create_time_slot, name='create_time_slot'),
    path('instructors/<int:instructor_id>/assign-time-slot/', views.assign_time_slot, name='assign_time_slot'),
    path('assign-zoom-link/<int:assignment_id>/', views.assign_zoom_link, name='assign_zoom_link'),
    path('password_reset/', PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    # path('forget_password', views.forget_password, name='forget_password'),

]
