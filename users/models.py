from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class UniversityStudent(models.Model):
    matric_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    year_admitted = models.IntegerField()
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.matric_number} - {self.first_name} {self.last_name}"

class CustomUser(AbstractUser):
    # Additional user fields
    # phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Mental health preferences
    preferred_name = models.CharField(max_length=100, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    has_mental_health_history = models.BooleanField(default=False)
    
    # Privacy settings
    allow_data_collection = models.BooleanField(
        default=True,
        help_text="Allow anonymized data to be used for improving the service"
    )
    
    def __str__(self):
        return f"{self.username} ({self.email})"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_record = models.OneToOneField(
        UniversityStudent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_profile"
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    last_mood_check = models.DateTimeField(null=True, blank=True)
    average_mood_score = models.FloatField(null=True, blank=True)

    def update_mood_stats(self):
        moods = self.user.moodentry_set.all()
        if moods.exists():
            self.last_mood_check = moods.latest('timestamp').timestamp
            self.average_mood_score = sum(m.score for m in moods) / moods.count()
            self.save()

    def __str__(self):
        return f"Profile of {self.user.username}"
    

from django.utils.timezone import now

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)  # Optional link to chat or detail page

    def __str__(self):
        return f"To {self.recipient.username}: {self.message[:50]}"