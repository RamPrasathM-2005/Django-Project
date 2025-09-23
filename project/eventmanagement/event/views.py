import io
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import Workshop, Enrollment, Attendance, Certificate
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings

# ---------------------------
# Member 1: Workshop listing & enrollment
# ---------------------------
def workshop_list(request):
    workshops = Workshop.objects.all().order_by("-date")
    return render(request, "event/workshops.html", {"workshops": workshops})

# Simple enroll view (for demo). In production, protect with login and checks.
def enroll_student(request, workshop_id, student_id):
    student = get_object_or_404(User, id=student_id)
    workshop = get_object_or_404(Workshop, id=workshop_id)
    Enrollment.objects.get_or_create(student=student, workshop=workshop)
    return redirect(reverse("event:workshop_list"))

# ---------------------------
# Member 2: Attendance marking (simple)
# ---------------------------
def mark_attendance(request, workshop_id, student_id, present):
    student = get_object_or_404(User, id=student_id)
    workshop = get_object_or_404(Workshop, id=workshop_id)
    # uses workshop.date as attendance date for simplicity
    Attendance.objects.update_or_create(
        student=student,
        workshop=workshop,
        date=workshop.date,
        defaults={"present": bool(int(present))},
    )
    return HttpResponse("Attendance updated")

# ---------------------------
# Member 3: Certificate generation (ReportLab)
# ---------------------------
def generate_certificate(request, student_id, workshop_id):
    student = get_object_or_404(User, id=student_id)
    workshop = get_object_or_404(Workshop, id=workshop_id)

    # You may want to check attendance thresholds before issuing certificate,
    # e.g. ensure Attendance present=True exists. For now, issue directly.

    # Create PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Draw a simple certificate layout
    p.setFont("Helvetica-Bold", 28)
    p.drawCentredString(width / 2, height - 120, "Certificate of Participation")

    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2, height - 170, "This is to certify that")

    name = f"{student.first_name} {student.last_name}".strip() or student.username
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 210, name)

    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2, height - 250, f"has successfully attended the workshop")
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 280, f"\"{workshop.title}\"")

    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2, height - 320, f"Date: {workshop.date}")

    # signature placeholder
    p.setFont("Helvetica", 12)
    p.drawString(80, 100, "______________________")
    p.drawString(80, 85, "Coordinator")

    p.showPage()
    p.save()
    buffer.seek(0)

    # Save to Certificate model and to FileField
    cert, created = Certificate.objects.get_or_create(student=student, workshop=workshop)
    filename = f"{slugify(student.username)}_{slugify(workshop.title)}.pdf"

    # Save FileField - need Django File object
    from django.core.files.base import ContentFile
    cert.pdf.save(filename, ContentFile(buffer.getvalue()), save=True)

    # Return PDF as response
    resp = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    resp["Content-Disposition"] = f'inline; filename="{filename}"'
    return resp

# ---------------------------
# Member 3: Analytics endpoints
# ---------------------------
def workshop_analytics_data(request):
    workshops = Workshop.objects.all().order_by("-date")
    data = []
    for w in workshops:
        total_enrolled = Enrollment.objects.filter(workshop=w).count()
        certificates_issued = Certificate.objects.filter(workshop=w).count()
        attendance_count = Attendance.objects.filter(workshop=w, present=True).count()
        data.append({
            "id": w.id,
            "title": w.title,
            "date": w.date.isoformat(),
            "enrolled": total_enrolled,
            "certificates": certificates_issued,
            "attendance": attendance_count,
        })
    return JsonResponse(data, safe=False)

def analytics_page(request):
    return render(request, "event/analytics.html")
