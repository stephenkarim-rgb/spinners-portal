import random
from django.shortcuts import render, redirect, get_object_or_get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from .models import CompanyUser, AttacheeProfile, DailyWork, AssignedTask
from .forms import AttacheeProfileForm, DailyWorkForm

def attachee_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = CompanyUser.objects.get(email=email)
        except CompanyUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})

        if user.is_locked:
            return render(request, 'login.html', {'error': 'Account locked! Maximum attempts exceeded. Contact your System Administrator.'})

        authenticated_user = authenticate(username=email, password=password)

        if authenticated_user is not None:
            # Code verification segment setup
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.login_attempts = 0
            user.save()
            
            # Outputs straight to your console terminal shell window
            send_mail(
                'Security Check: OTP Verification Access Token',
                f'Your validation verification token entry code is: {otp}',
                'admin@company.com',
                [user.email],
                fail_silently=False,
            )
            request.session['pre_verified_user_id'] = user.id
            return redirect('verify_otp')
        else:
            user.login_attempts += 1
            if user.login_attempts >= 4:
                user.is_locked = True
                error = 'Account locked! Maximum attempts exceeded. Contact your System Administrator.'
            else:
                error = f'Invalid password entry details. Attempts remaining: {4 - user.login_attempts}'
            user.save()
            
    return render(request, 'login.html', {'error': error})

def verify_otp(request):
    error = None
    user_id = request.session.get('pre_verified_user_id')
    if not user_id:
        return redirect('login')
        
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        user = CompanyUser.objects.get(id=user_id)
        
        if user.otp == otp_input:
            user.is_verified = True
            user.save()
            login(request, user)
            del request.session['pre_verified_user_id']
            return redirect('dashboard')
        else:
            error = "Invalid validation token provided. Try again."
            
    return render(request, 'otp_verify.html', {'error': error})

@login_required
def dashboard(request):
    profile, created = AttacheeProfile.objects.get_or_create(user=request.user)
    tasks = AssignedTask.objects.filter(attachee=request.user)
    work_history = DailyWork.objects.filter(attachee=request.user).order_by('-date')
    
    if request.method == 'POST':
        work_form = DailyWorkForm(request.POST, request.FILES)
        if work_form.is_valid():
            work_item = work_form.save(commit=False)
            work_item.attachee = request.user
            work_item.save()
            return redirect('dashboard')
    else:
        work_form = DailyWorkForm()
        
    storage_gb = round(profile.storage_used / (1024**3), 4)
    
    context = {
        'profile': profile,
        'tasks': tasks,
        'work_history': work_history,
        'work_form': work_form,
        'storage_gb': storage_gb
    }
    return render(request, 'dashboard.html', context)

@login_required
def edit_profile(request):
    profile, created = AttacheeProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AttacheeProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AttacheeProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})

def log_out(request):
    logout(request)
    return redirect('login')

# 📊 Admin Performance PDF Export Route Engine
@login_required
def export_pdf_report(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized view attempt", status=401)
        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Attachee_Corporate_Report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph("<b>System Attachment Framework - Summary Performance Report</b>", styles['Title']))
    story.append(Spacer(1, 15))

    attachees = CompanyUser.objects.filter(is_attachee=True)

    for attachee in attachees:
        profile, _ = AttacheeProfile.objects.get_or_create(user=attachee)
        
        info_table = [
            [f"Attachee: {attachee.get_full_name() or attachee.username}", f"School: {profile.school_name or 'N/A'}"],
            [f"Corporate Mail: {attachee.email}", f"Adm Number: {profile.school_admission_number or 'N/A'}"],
            [f"Course Path: {profile.program_of_study or 'N/A'}", f"Storage Allocations: {round(profile.storage_used/(1024**3), 2)} GB / 30 GB"]
        ]
        t_info = Table(info_table, colWidths=[250, 250])
        t_info.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.white),
            ('PADDING', (0,0), (-1,-1), 6),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9)
        ]))
        story.append(t_info)
        story.append(Spacer(1, 10))

        works = DailyWork.objects.filter(attachee=attachee).order_by('-date')
        work_table_data = [["Log Date", "Executed Daily Work Run Details"]]
        
        for w in works:
            work_table_data.append([w.date.strftime('%Y-%m-%d'), Paragraph(w.work_description, styles['Normal'])])

        if len(work_table_data) > 1:
            t_work = Table(work_table_data, colWidths=[90, 410])
            t_work.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 5),
                ('FONTSIZE', (0,0), (-1,-1), 9)
            ]))
            story.append(t_work)
        else:
            story.append(Paragraph("<i>No tasks documented or uploaded over operational timelines for this student yet.</i>", styles['Normal']))
            
        story.append(Spacer(1, 25))

    doc.build(story)
    return response