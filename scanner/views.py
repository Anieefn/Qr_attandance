from io import BytesIO

import qrcode
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from datetime import timedelta
from .models import Register, Report, Attendance
# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to find matching user
        user = Register.objects.filter(username=username, password=password).first()

        if user:
            # Redirect based on role
            if user.role == 'student':
                return redirect('student', userid=user.id)
            elif user.role == 'teacher':
                return redirect('home', userid=user.id)
        else:
            # Only show error if form is submitted AND credentials are wrong
            return render(request, 'login.html', {
                "error_message": "Username or password is incorrect"
            })

    # GET request (loading page) — no error message
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        roll_number = request.POST['roll_number']
        image = request.FILES.get('image')

        # Generate QR code
        qr_img = qrcode.make(roll_number)
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_file = ContentFile(buffer.getvalue(), name=f"{roll_number}_qr.png")

        # Save user with QR
        user = Register(
            username=username,
            password=password,
            email=email,
            roll_number=roll_number,
            image=image,
            qr=qr_file
        )
        user.save()

        print("Sign in successful")
        return render(request, 'login.html')

    return render(request, 'signup.html')

def teacher(request, userid):
    # Get teacher's own data
    user = get_object_or_404(Register, id=userid)

    # Get all students
    students = Register.objects.filter(role='student')

    student_data = []
    for student in students:
        attendance = Attendance.objects.filter(roll_number=student.roll_number).first()
        report = Report.objects.filter(roll_number=student.roll_number).first()

        student_data.append({
            "username": student.username,
            "roll_number": student.roll_number,
            "image": getattr(student, "image", None),  # only works if you add an image field
            "attendance_present": attendance.present if attendance else None,
            "attendance_date": attendance.date if attendance else None,
            "report_date": report.date if report else None
        })

    return render(request, 'home.html', {
        "userid": userid,
        "student_data": student_data,

    })


def attendance(request,userid):
    pre = 0
    error_message = None
    post = None

    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')

        # Step 1: Validate roll number
        user = Register.objects.filter(roll_number=roll_number).first()
        if not user:
            error_message = "Roll number not found."
            return render(request, 'scan.html', {
                "error_message": error_message,
                "userid": userid
            })

        # Step 2: Check today's report
        today = now().date()
        report_entry = Report.objects.filter(roll_number=roll_number).order_by('-date').first()

        if report_entry and report_entry.date == today:
            pre -= 4
        else:
            pre += 2

        # Step 3: Handle attendance
        current_time = now()
        attendance_entry = Attendance.objects.filter(roll_number=roll_number).first()

        if attendance_entry:
            time_diff = current_time - attendance_entry.date
            if time_diff >= timedelta(minutes=30):
                attendance_entry.present += pre
                attendance_entry.date = current_time
                attendance_entry.save()
                post = user
            else:
                error_message = "Attendance already marked in the last 30 minutes."
        else:
            Attendance.objects.create(
                roll_number=roll_number,
                present=pre,
                date=current_time
            )
            post = user

    return render(request, 'scan.html', {
        "pre": pre,
        "error_message": error_message,
        "post": post,
        "userid": userid
    })

def student_dashboard(request, userid):
    # Get the logged-in student's data
    student = get_object_or_404(Register, id=userid, role='student')

    # Get attendance and report data
    attendance = Attendance.objects.filter(roll_number=student.roll_number).first()
    report = Report.objects.filter(roll_number=student.roll_number).first()

    student_data = {
        "username": student.username,
        "roll_number": student.roll_number,
        "image": getattr(student, "image", None),
        "qr": getattr(student, "qr", None),
        "attendance_present": attendance.present if attendance else None,
        "attendance_date": attendance.date if attendance else None,
        "report_date": report.date if report else None
    }

    return render(request, 'student_home.html', {
        "student_data": student_data,
        "userid": userid
    })

def report(request,userid):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        reports=Report(roll_number=roll_number)
        reports.save()
    return render(request,'report.html',{'userid': userid})

def logout(request):
    return render(request,'login.html')