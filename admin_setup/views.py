from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group, User
from home_setup.models import StudentProfile, StaffProfile, Mark, Subject, Department, Position
from .forms import AdminRegistrationForm, StaffRegistrationForm, StaffProfileForm, PositionForm, DepartmentForm
from profile_setup.models import Profile
from django.db.models import Max, Q
from django.contrib.auth.models import Group, User
from home_setup.forms import StudentCreateForm, StudentProfileForm, MarkForm, EditStudentUserForm
from .models import AdminProfile

# Create your views here.

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def admin_home(request):
    total_users = User.objects.count()
    total_students = StudentProfile.objects.count()
    total_staff = StaffProfile.objects.count()

    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_staff': total_staff,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def manage_students(request):
    selected_dept = request.GET.get('department')

    departments = Department.objects.all()

    if selected_dept:
        students = StudentProfile.objects.filter(department_id=selected_dept)
    else:
        students = StudentProfile.objects.all()

    return render(request, 'manage_students.html', {
        'students': students,
        'departments': departments,
        'selected_dept': selected_dept,
    })

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def delete_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    username = student.user.username

    student.user.delete()

    messages.success(request, f"Student '{username}' has been deleted successfully.")
    return redirect('manage_students')

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def manage_staff(request):
    selected_dept = request.GET.get('department')

    departments = Department.objects.all()

    if selected_dept:
        staff_members = StaffProfile.objects.filter(department_id=selected_dept)
    else:
        staff_members = StaffProfile.objects.all()

    return render(request, 'manage_staff.html', {
        'staff_members': staff_members,
        'departments': departments,
        'selected_dept': selected_dept,
    })

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def delete_staff(request, employee_id):
    staff = get_object_or_404(StaffProfile, id=employee_id)
    username = staff.user.username

    staff.user.delete()
    messages.success(request, f"staff {username} has been deleted.")

    return redirect('manage_staff')

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def manage_users(request):
    selected_group = request.GET.get('group')
    search_query = request.GET.get('search', '')

    groups = Group.objects.all()

    users = User.objects.all()

    if selected_group:
        users = User.objects.filter(groups__id=selected_group)
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
        
    return render(request, 'manage_users.html', {
        'users': users,
        'groups': groups,
        'selected_group': selected_group,
        'search_query': search_query,
    })

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True 
            user.is_superuser = True
            user.save()

            group, created = Group.objects.get_or_create(name='admin')
            user.groups.add(group)

            Profile.objects.create(
                user=user,
                user_type="admin"
            )

            last_admin = AdminProfile.objects.order_by('id').last()
            new_id = 1 if not last_admin else last_admin.id + 1
            admin_id = f"ADM{new_id:03d}"

            AdminProfile.objects.create(
                user=user,
                admin_id=admin_id
            )

            messages.success(request, "Admin registered successfully!")
            return redirect('manage_users')
    else:
        form = AdminRegistrationForm()

    return render(request, 'admin_register.html', {'form': form})


@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def admin_register_student(request):
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
            return redirect('manage_students')
    else:
        form = StudentCreateForm()
    
    return render(request, 'admin_register_student.html', {'form': form})

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def admin_register_staff(request):
    if request.method == 'POST':
        user_form = StaffRegistrationForm(request.POST)
        profile_form = StaffProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.is_staff = True
            user.save()

            staff_profile = profile_form.save(commit=False)
            staff_profile.user = user
            staff_profile.save()

            group, created = Group.objects.get_or_create(name='staff')
            user.groups.add(group)

            Profile.objects.create(
                user=user,
                user_type='staff',
                department=staff_profile.department  
            )

            return redirect('manage_staff')

    else:
        user_form = StaffRegistrationForm()
        profile_form = StaffProfileForm()

    return render(request, 'admin_register_staff.html', {'user_form': user_form, 'profile_form': profile_form,})

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def manage_department(request):
    departments = Department.objects.all()
    form = DepartmentForm()

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_department')

    return render(request, "manage_department.html", {
        "departments": departments,
        "form": form
    })


@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def delete_department(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    dept.delete()
    return redirect('manage_department')


@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def manage_position(request):
    positions = Position.objects.all()
    form = PositionForm()

    if request.method == "POST":
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_position')

    return render(request, "manage_position.html", {
        "positions": positions,
        "form": form
    })

@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def delete_position(request, pos_id):
    pos = get_object_or_404(Position, id=pos_id)
    pos.delete()
    return redirect('manage_position')


@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)

    if user.is_superuser:
        messages.error(request, "Superuser cannot be deleted.")
        return redirect('manage_users')

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('manage_users')


@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def department_subject_overview(request):
    departments = Department.objects.all().prefetch_related('subjects')
    return render(request, 'department_subject_overview.html', {'departments': departments})


@login_required(login_url='/login/admin/')
@user_passes_test(is_admin)
def add_subject(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)

    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Subject.objects.create(name=name, department=department)
            return redirect('dept_subject_overview')

    return render(request, 'add_subject.html', {'department': department})
