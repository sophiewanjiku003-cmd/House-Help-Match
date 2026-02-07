from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (UserProfile, HouseHelpProfile, JobPosting, Application, 
                     Review, Message, OTPVerification, Location)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type']
        widgets = {}

    def __init__(self, *args, **kwargs):
        """Remove the 'manager' option from the user_type choices on public registration forms.
        Admin can still create manager users via the Django admin because the model choices remain unchanged.
        """
        super().__init__(*args, **kwargs)
        try:
            # Filter out the manager choice for the form field
            orig_choices = list(self.fields['user_type'].choices)
            filtered = [c for c in orig_choices if str(c[0]) != 'manager']
            self.fields['user_type'].choices = filtered
        except Exception:
            pass

class HouseHelpProfileForm(forms.ModelForm):
    class Meta:
        model = HouseHelpProfile
        fields = ['skills', 'experience', 'skill_level', 'hourly_rate', 'bio', 'is_available', 'cv']
        labels = {
            'hourly_rate': 'Daily Pay (KES)'
        }
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Cleaning, Cooking, Child Care, Elderly Care'}),
            'bio': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell employers about your experience and qualifications...'}),
        }

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'category', 'description', 'requirements', 'location', 
                 'salary', 'job_type', 'hours_per_week']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Describe the job responsibilities...'}),
            'requirements': forms.Textarea(attrs={'rows': 4, 'placeholder': 'List required skills and qualifications...'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Write your cover letter here...'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'profile_pic']


# ==================== NEW FORMS ====================

class ReviewForm(forms.ModelForm):
    """Form for rating and reviewing househelps"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your experience with this househelp...',
                'class': 'form-control'
            }),
        }
        labels = {
            'rating': 'Rating',
            'comment': 'Comment (Optional)',
        }


class MessageForm(forms.ModelForm):
    """Form for sending messages"""
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': 'Message subject',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Type your message here...',
                'class': 'form-control'
            }),
        }


class OTPVerificationForm(forms.Form):
    """Form for OTP verification"""
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit OTP',
            'class': 'form-control',
            'maxlength': '6',
            'autocomplete': 'off'
        }),
        label='Enter OTP'
    )


class LocationForm(forms.ModelForm):
    """Form for location preferences"""
    class Meta:
        model = Location
        fields = ['city', 'radius_km']
        widgets = {
            'city': forms.TextInput(attrs={
                'placeholder': 'Enter your city/location',
                'class': 'form-control'
            }),
            'radius_km': forms.NumberInput(attrs={
                'min': 5,
                'max': 100,
                'class': 'form-control'
            }),
        }
        labels = {
            'city': 'City/Location',
            'radius_km': 'Search Radius (km)',
        }


class JobFilterForm(forms.Form):
    """Form for filtering jobs by location and other criteria"""
    SORT_CHOICES = [
        ('recent', 'Most Recent'),
        ('salary_high', 'Highest Salary'),
        ('salary_low', 'Lowest Salary'),
    ]
    
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by location...',
            'class': 'form-control'
        })
    )
    radius_km = forms.IntegerField(
        required=False,
        initial=10,
        widget=forms.NumberInput(attrs={
            'min': 5,
            'max': 100,
            'class': 'form-control'
        })
    )
    min_salary = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Minimum salary',
            'class': 'form-control'
        })
    )
    max_salary = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Maximum salary',
            'class': 'form-control'
        })
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )