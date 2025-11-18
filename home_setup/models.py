from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.core.validators import MinValueValidator
from django.utils.text import slugify

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,  related_name='subjects')

    def __str__(self):
        return f"{self.code}: {self.name} ({self.department.name})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new or not self.code:
            dept_abbr = slugify(self.department.name).upper()[:3]

            self.code = f"{dept_abbr}-{self.pk:04d}"
            kwargs.pop('force_insert', None)
            super().save(update_fields=['code'], *args, **kwargs)


class Position(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.roll_number:
            last_roll = (
                StudentProfile.objects.filter(department=self.department)
                .aggregate(Max('id'))['id__max']
            )
            next_id = (last_roll or 0) + 1
            dept_code = self.department.name[:3].upper()
            self.roll_number = f"{dept_code}{next_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"

class Mark(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}"

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    employee_id = models.CharField(max_length=20, unique=True, editable=False)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    date_joined = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_profile = StaffProfile.objects.all().order_by('id').last()
            if last_profile:
                last_id = int(last_profile.employee_id.replace("EMP", ""))
                new_id = last_id + 1
            else:
                new_id = 1

            self.employee_id = f"EMP{new_id:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.department}"