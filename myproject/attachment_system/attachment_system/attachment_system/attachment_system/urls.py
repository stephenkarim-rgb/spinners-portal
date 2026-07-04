from django.urls import path
from . import views

urlpatterns = [
    path('', views.attachee_login, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.log_out, name='logout'),
    path('admin/export-pdf/', views.export_pdf_report, name='export_pdf'),
]