from django.contrib import admin
from .models import StudentProfile, Subject, Mark, StaffProfile

# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(Subject)
admin.site.register(Mark)
admin.site.register(StaffProfile)