# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth import get_user_model


class StudentVerificationForm(forms.Form):
    matric_number = forms.CharField(
        max_length=20,
        label="Matriculation Number",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. 210591032',
            'class': 'form-control',
            'autofocus': 'autofocus'
        })
    )

    def clean_matric_number(self):
        matric_number = self.cleaned_data.get('matric_number').upper().strip()
        try:
            student = UniversityStudent.objects.get(matric_number=matric_number)
            
            # Check if already registered
            if hasattr(student, 'linked_profile'):
                raise ValidationError(
                    "This matric number has already been used to create an account. "
                    "If you've forgotten your password, use the reset option."
                )
            return student

        except UniversityStudent.DoesNotExist:
            raise ValidationError(
                "This matric number was not found in our records. "
                "Please check it or contact your university admin."
            )

class StudentRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password',
            'class': 'form-control'
        }),
        label='Password',
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'form-control'
        }),
        label='Confirm Password',
    )
    
    class Meta:
        model = CustomUser
        fields = ('password1', 'password2')
    
    def __init__(self, *args, student_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_data = student_data
        
    def save(self, commit=True):
        user = super().save(commit=False)

        if self.student_data:
            user.username = self.student_data['matric_number'].upper()

            if commit:
                user.save()

                profile, _ = UserProfile.objects.get_or_create(user=user)

                try:
                    student_obj = UniversityStudent.objects.get(
                        matric_number=self.student_data['matric_number']
                    )
                    profile.student_record = student_obj
                    profile.save()
                except UniversityStudent.DoesNotExist:
                    pass

        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Matric Number',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your matric number',
            'class': 'form-control',
        })
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control',
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().upper()

        # Ensure matric number exists as a username
        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            raise ValidationError("This matric number is not registered.")
        return username
    

class CombinedProfileForm(forms.ModelForm):
    # Fields from CustomUser
    preferred_name = forms.CharField(required=False, max_length=100)
    emergency_contact = forms.CharField(required=False, max_length=100)
    allow_data_collection = forms.BooleanField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance')
        super().__init__(*args, **kwargs)

        # Initialize fields from CustomUser
        self.fields['preferred_name'].initial = self.user_instance.preferred_name
        self.fields['emergency_contact'].initial = self.user_instance.emergency_contact
        self.fields['allow_data_collection'].initial = self.user_instance.allow_data_collection

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Save related CustomUser fields
            self.user_instance.preferred_name = self.cleaned_data['preferred_name']
            self.user_instance.emergency_contact = self.cleaned_data['emergency_contact']
            self.user_instance.allow_data_collection = self.cleaned_data['allow_data_collection']
            self.user_instance.save()
        return profile

    