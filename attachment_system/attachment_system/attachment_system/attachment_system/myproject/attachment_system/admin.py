from django.contrib import admin
from .models import CompanyUser, AttacheeProfile, DailyWork, AssignedTask, SystemControl

@admin.action(description='Reset and Unlock chosen locked accounts')
def unlock_user_accounts(modeladmin, request, queryset):
    queryset.update(is_locked=False, login_attempts=0)

class UserAdminConfig(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_attachee', 'login_attempts', 'is_locked']
    search_fields = ['email', 'username']
    actions = [unlock_user_accounts]

class ProfileAdminConfig(admin.ModelAdmin):
    list_display = ['user', 'school_name', 'program_of_study', 'can_edit_profile', 'storage_used']
    list_editable = ['can_edit_profile']

admin.site.register(CompanyUser, UserAdminConfig)
admin.site.register(AttacheeProfile, ProfileAdminConfig)
admin.site.register(DailyWork)
admin.site.register(AssignedTask)
admin.site.register(SystemControl)