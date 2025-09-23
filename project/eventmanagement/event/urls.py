from django.urls import path
from . import views

app_name = "event"

urlpatterns = [
    # Member 1: listing & enrollment
    path("workshops/", views.workshop_list, name="workshop_list"),
    path("enroll/<int:workshop_id>/<int:student_id>/", views.enroll_student, name="enroll_student"),

    # Member 2: attendance
    path("attendance/<int:workshop_id>/<int:student_id>/<int:present>/", views.mark_attendance, name="mark_attendance"),

    # Member 3: certificate & analytics
    path("certificate/<int:student_id>/<int:workshop_id>/", views.generate_certificate, name="generate_certificate"),
    path("analytics-data/", views.workshop_analytics_data, name="workshop_analytics_data"),
    path("analytics/", views.analytics_page, name="analytics_page"),
]
