from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, TimeSlot
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
class CustomUserCreationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    class Meta:
        model = CustomUser
        fields = ('full_name', 'age', 'phone_number', 'gender', 'country', 'email')

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not 1 <= age <= 100:
            raise ValidationError(_('Age must be between 1 and 100'))
        return age

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError(_('Phone number must be a 10-digit number'))
        return phone_number

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not isinstance(country, str):
            raise ValidationError(_('Country must be a string'))
        return country

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # You can add more complex email validation if needed
        if not forms.EmailField().clean(email):
            raise ValidationError(_('Invalid email format'))
        return email

from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'price_individual', 'price_group', 'from_age', 'to_age']
    # Check for blank or None values
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        price_individual = cleaned_data.get('price_individual')
        price_group = cleaned_data.get('price_group')
        from_age = cleaned_data.get('from_age')
        to_age = cleaned_data.get('to_age')

        # Check for blank or None values
        if not title:
            self.add_error('title', 'Title is required.')

        if not price_individual:
            self.add_error('price_individual', 'Price individual is required.')
        
        if not price_group:
            self.add_error('price_group', 'Price group is required.')

        if not from_age:
            self.add_error('from_age', 'From age is required.')
        elif not isinstance(from_age, int) or from_age <= 0 or from_age >= 100:
            self.add_error('from_age', 'From age must be a valid integer greater than 0 and less than 100.')

        if not to_age:
            self.add_error('to_age', 'To age is required.')
        elif not isinstance(to_age, int) or to_age <= 0 or to_age >= 100:
            self.add_error('to_age', 'To age must be a valid integer greater than 0 and less than 100.')

        if from_age is not None and to_age is not None and from_age >= to_age:
            self.add_error('from_age', 'From age must be less than To age.')

        return cleaned_data


from django import forms
from .models import Instructor  # Import the Instructor model

class InstructorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select())

    class Meta:
        model = Instructor
        fields = ('full_name', 'age', 'phone_number', 'gender', 'country', 'email', 'is_instructor', 'password')

    def clean_age(self):
        age = self.cleaned_data['age']
        if age <= 1 or age >= 100:
            raise forms.ValidationError('Age must be between 1 and 99.')
        return age

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError('Phone number must be a 10-digit number.')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email or '.' not in email:
            raise forms.ValidationError('Enter a valid email address.')
        return email

   
    
from django import forms
from .models import TimeSlot

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = '__all__'
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class TimeSlotAssignmentForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    timeslot = forms.ModelChoiceField(queryset=TimeSlot.objects.filter())