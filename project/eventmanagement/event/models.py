from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ---------------------------
# Member 1 - Workshop & Enrollment
# ---------------------------
class Workshop(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    capacity = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(default=timezone.now, editable=False)


    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "workshop")

    def __str__(self):
        return f"{self.student.username} -> {self.workshop.title}"

# ---------------------------
# Member 2 - Attendance Tracking
# ---------------------------
class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    date = models.DateField()

    class Meta:
        unique_together = ("student", "workshop", "date")

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.student.username} - {self.workshop.title} ({status})"

# ---------------------------
# Member 3 - Certificate & Analytics
# ---------------------------
class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    pdf = models.FileField(upload_to="certificates/", blank=True, null=True)

    class Meta:
        unique_together = ("student", "workshop")

    def __str__(self):
        return f"{self.student.username} - {self.workshop.title}"
