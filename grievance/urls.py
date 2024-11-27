from django.urls import path

from .views import (
    HostelWiseReport,
    TicketApprovalView,
    TicketCreateView,
    TicketImageView,
    TicketShowView,
)

urlpatterns = [
    path("create_ticket/", TicketCreateView.as_view()),
    path("grievance/<str:pk>/", TicketShowView.as_view()),
    path("action/<str:pk>/", TicketApprovalView.as_view()),
    path("image_upload/", TicketImageView.as_view()),
    path("report/", HostelWiseReport.as_view()),
]
