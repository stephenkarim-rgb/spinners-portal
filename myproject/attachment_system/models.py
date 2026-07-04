from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class CompanyUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_attachee = models.BooleanField(default=True)
    login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class AttacheeProfile(models.Model):
    user = models.OneToOneField(CompanyUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    school_admission_number = models.CharField(max_length=50)
    school_name = models.CharField(max_length=100)
    program_of_study = models.CharField(max_length=100)
    
    can_edit_profile = models.BooleanField(default=False)
    storage_used = models.BigIntegerField(default=0)
    MAX_STORAGE = 32212254720 # Exactly 30 Gigabytes in Bytes

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.school_admission_number})"

class DailyWork(models.Model):
    attachee = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='daily_reports')
    date = models.DateField(auto_now_add=True)
    work_description = models.TextField()
    uploaded_file = models.FileField(upload_to='work_submissions/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.uploaded_file:
            file_size = self.uploaded_file.size
            profile, created = AttacheeProfile.objects.get_or_create(user=self.attachee)
            if profile.storage_used + file_size > profile.MAX_STORAGE:
                raise ValidationError("File submission rejected! Your 30GB individual storage space layout is fully exhausted.")
            profile.storage_used += file_size
            profile.save()
        super().save(*args, **kwargs)

class AssignedTask(models.Model):
    attachee = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='assigned_tasks')
    task_title = models.CharField(max_length=200)
    task_description = models.TextField()
    assigned_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

class SystemControl(models.Model):
    is_system_closed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Global System Control Switch"
        verbose_name_plural = "Global System Control Switches"