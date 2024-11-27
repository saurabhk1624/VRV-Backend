from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.functions import get_user_role
from common.models import Dropdown, LeftPanel, Role
from common.response import CustomResponse
from common.serializers import DropdownSerializer, LeftPanelSerializer


class DropdownListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DropdownSerializer

    def get_queryset(self, request):
        user = request.user.id
        role_name, role, hostel = get_user_role(user)
        request_type = self.request.query_params.get("request_type", None)
        if request_type:
            if request_type == "HOSTEL":
                return Dropdown.objects.filter(id__in=hostel)
            else:
                if request_type == "ALLHOSTEL":
                    request_type = "HOSTEL"
                parent = Dropdown.objects.filter(field=request_type).first()
                if parent:
                    return Dropdown.objects.filter(parent=parent)
                else:
                    return Dropdown.objects.none()
        else:
            return Dropdown.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)

        if not queryset.exists():
            return Response(
                {"message": "No dropdowns found for the provided request_type."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LeftPanelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        query = list(
            Role.objects.filter(user=request.user).values_list("role", flat=True)
        )
        left_panel_items = LeftPanel.objects.filter(
            role__in=query, parent__isnull=True, status=True
        ).order_by("priority")
        serializer = LeftPanelSerializer(left_panel_items, many=True)
        return CustomResponse(message=serializer.data, status=200)
