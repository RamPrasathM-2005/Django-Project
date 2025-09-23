from django.contrib import admin
from .models import Workshop, Enrollment, Attendance, Certificate

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "capacity", "created_at")
    search_fields = ("title",)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "workshop", "enrolled_date")
    list_filter = ("workshop",)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "workshop", "date", "present")
    list_filter = ("workshop", "date", "present")

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("student", "workshop", "issued_date")
    readonly_fields = ("issued_date",)
