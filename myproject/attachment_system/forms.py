from django import forms
from .models import AttacheeProfile, DailyWork


class AttacheeProfileForm(forms.ModelForm):
    class Meta:
        model = AttacheeProfile
        fields = ['profile_picture', 'school_admission_number', 'school_name', 'program_of_study']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.can_edit_profile:
            self.fields['school_admission_number'].disabled = True
            self.fields['school_name'].disabled = True
            self.fields['program_of_study'].disabled = True


class DailyWorkForm(forms.ModelForm):
    class Meta:
        model = DailyWork
        fields = ['work_description', 'uploaded_file']
