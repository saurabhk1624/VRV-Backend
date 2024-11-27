from django.urls import path

from .views import DropdownListView, LeftPanelAPIView

urlpatterns = [
    path("dropdown/", DropdownListView.as_view()),
    path("left_panel/", LeftPanelAPIView.as_view()),
]
