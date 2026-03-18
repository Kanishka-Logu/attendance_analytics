from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Attendance
from datetime import date, timedelta


def dashboard(request):
    total_students = Student.objects.count()
    today = date.today()
    present_today = Attendance.objects.filter(date=today, status='Present').count()
    absent_today = Attendance.objects.filter(date=today, status='Absent').count()
    all_students = Student.objects.all()
    low_attendance = [s for s in all_students if s.attendance_percentage() < 75]
    context = {
        'total_students': total_students,
        'present_today': present_today,
        'absent_today': absent_today,
        'low_attendance': low_attendance,
        'today': today,
    }
    return render(request, 'dashboard.html', context)


def students(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll = request.POST.get('roll_number')
        email = request.POST.get('email', '')
        if name and roll:
            Student.objects.get_or_create(
                roll_number=roll,
                defaults={'name': name, 'email': email}
            )
            messages.success(request, f"Student '{name}' added successfully!")
        return redirect('students')
    all_students = Student.objects.all().order_by('roll_number')
    return render(request, 'students.html', {'students': all_students})


def delete_student(request, pk):
    Student.objects.filter(pk=pk).delete()
    messages.success(request, "Student deleted.")
    return redirect('students')


def mark_attendance(request):
    all_students = Student.objects.all().order_by('roll_number')
    today = date.today()
    if request.method == 'POST':
        selected_date = request.POST.get('date', str(today))
        for student in all_students:
            status = request.POST.get(f'status_{student.id}', 'Absent')
            Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={'status': status}
            )
        messages.success(request, f"Attendance saved for {selected_date}!")
        return redirect('mark_attendance')
    existing = {a.student_id: a.status for a in Attendance.objects.filter(date=today)}
    student_data = [{'student': s, 'status': existing.get(s.id, '')} for s in all_students]
    return render(request, 'mark_attendance.html', {
        'student_data': student_data,
        'today': today,
    })


def analytics(request):
    all_students = Student.objects.all()
    data = []
    for s in all_students:
        total = Attendance.objects.filter(student=s).count()
        present = Attendance.objects.filter(student=s, status='Present').count()
        absent = total - present
        data.append({
            'student': s,
            'total': total,
            'present': present,
            'absent': absent,
            'percentage': s.attendance_percentage(),
        })
    trend_labels, trend_present, trend_absent = [], [], []
    for i in range(6, -1, -1):
        d = date.today() - timedelta(days=i)
        trend_labels.append(d.strftime('%b %d'))
        trend_present.append(Attendance.objects.filter(date=d, status='Present').count())
        trend_absent.append(Attendance.objects.filter(date=d, status='Absent').count())
    return render(request, 'analytics.html', {
        'data': data,
        'trend_labels': trend_labels,
        'trend_present': trend_present,
        'trend_absent': trend_absent,
    })