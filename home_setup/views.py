from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import StudentProfile, Mark, Subject, StaffProfile, Department
from django.contrib.auth.models import Group, User
from .forms import StudentCreateForm, StudentProfileForm, MarkForm, EditStudentUserForm
from django.contrib import messages
from profile_setup.models import Profile
from django.db.models import Max
from django.urls import reverse
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
@login_required(login_url='/login/student/')
def student_home(request):
    student = StudentProfile.objects.get(user=request.user)
    marks = Mark.objects.filter(student=student).select_related('subject')

    context = {
        'student': student,
        'marks': marks,
    }

    return render(request, 'student_home.html', context) 


def is_staff(user):
    return user.groups.filter(name='staff').exists()

@never_cache
@login_required(login_url='/login/staff/')
@user_passes_test(is_staff)
def staff_home(request):
    profile = StaffProfile.objects.get(user=request.user)
    department = profile.department

    departments = Department.objects.all()

    selected_dept = request.GET.get("department", department.id)

    if selected_dept:
        students = StudentProfile.objects.filter(department_id=selected_dept)
    else:
        students = StudentProfile.objects.all()

    return render(request, 'staff_home.html', {
        'students': students,
        'department': department,
        'departments': departments,
        'selected_dept': selected_dept,
    })

@never_cache
@login_required(login_url='/login/staff/')
@user_passes_test(is_staff)
def edit_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    marks = Mark.objects.filter(student=student)
    
    if request.method == 'POST':
        student_form = EditStudentUserForm(request.POST, instance=student.user)
        if student_form.is_valid():
            student_form.save()
            messages.success(request, "Student details updated successfully.")
            return redirect(f"{reverse('staff_home')}?department={student.department.id}")
    else:
        student_form = EditStudentUserForm(instance=student.user)

    return render(request, 'edit_student.html', {
        'student_form': student_form,
        'student': student,
        'marks': marks,
    })

@never_cache
@login_required(login_url='/login/staff/')
@user_passes_test(is_staff)
def edit_mark(request, mark_id):
    mark = get_object_or_404(Mark, id=mark_id)
    if request.method == 'POST':
        form = MarkForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            messages.success(request, "Mark updated successfully.")
            return redirect('edit_student', student_id=mark.student.id)
    else:
        form = MarkForm(instance=mark)

    return render(request, 'edit_mark.html', {'form': form, 'mark': mark})

@never_cache
@login_required(login_url='/login/staff/')
@user_passes_test(is_staff)
def add_student(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)

            last_roll = (
                StudentProfile.objects.filter(department=student.department)
                .aggregate(Max('id'))['id__max']
            )
            next_id = (last_roll or 0) + 1
            dept_code = student.department.name[:3].upper()
            student.roll_number = f"{dept_code}{next_id:03d}"

            student.save()

            group, created = Group.objects.get_or_create(name='student')
            student.user.groups.add(group)

            Profile.objects.create(
                user=student.user,
                user_type='student',
                department=student.department
            )

            messages.success(
                request,
                f"New student added successfully! Roll No: {student.roll_number}"
            )
            return redirect('staff_home')
    else:
        form = StudentCreateForm()
    
    return render(request, 'add_student.html', {'form': form})

@never_cache
@login_required(login_url='/login/staff/')
@user_passes_test(is_staff)
def add_mark(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)

    if request.method == 'POST':
        form = MarkForm(request.POST, student=student)

        if form.is_valid():
            subject = form.cleaned_data['subject']

            if Mark.objects.filter(student=student, subject=subject).exists():
                messages.warning(request, "Marks for this subject already exist.")
                return redirect('edit_student', student_id=student.id)

            new_mark = form.save(commit=False)
            new_mark.student = student
            new_mark.save()

            messages.success(request, "New marks added successfully.")
            return redirect('edit_student', student_id=student.id)

    else:
        form = MarkForm(student=student)

    return render(request, 'add_mark.html', {'form': form, 'student': student})

@never_cache
@login_required(login_url='/login/staff/')
@user_passes_test(is_staff)
def delete_mark(request, mark_id):
    mark = get_object_or_404(Mark, id=mark_id)
    student_id = mark.student.id
    mark.delete()
    messages.success(request, "Subject & mark deleted successfully.")
    return redirect('edit_student', student_id=student_id)
