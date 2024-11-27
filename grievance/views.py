import json
from datetime import datetime

from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.functions import get_user_role, role_permission
from common.models import ActionNum, Dropdown
from common.response import BadResponse, CustomResponse
from grievance.models import Ticket, TicketApproval

from .serializers import (
    TicketApprovalSerializer,
    TicketImageSerializer,
    TicketSerializer,
    TicketShowSerializer,
)


class TicketImageView(
    APIView
):  # Api to save image regarding grievances accessible only to student
    permission_classes = [role_permission("STUDENT")]

    def post(self, request, *args, **kwargs):
        serializer = TicketImageSerializer(
            data=request.data, context={"user_id": request.user}
        )
        if serializer.is_valid():
            serializer.save(added_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketCreateView(APIView):  # Api to create grievances accessible only to student
    permission_classes = [role_permission("STUDENT")]

    def post(self, request, *args, **kwargs):
        user = request.user.id
        role_name, role, hostel = get_user_role(user)
        serializer = TicketSerializer(
            data=request.data, context={"user": user, "hostel": hostel[0]}
        )
        if serializer.is_valid():
            grievances = list(
                Dropdown.objects.filter(parent__field="MESS")
                .exclude(parent__isnull=True)
                .values_list("id", flat=True)
            )
            grievance = serializer.validated_data["grievance"]
            serializer.save()
            message = "Grievance applied Successfully!"
            return CustomResponse(message=message, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketShowView(APIView):  # api only accessible to warden
    permission_classes = [role_permission("WARDEN")]

    def get(self, request, pk):
        user = request.user.id
        role_name, role, hostel = get_user_role(user)
        grievances = Ticket.objects.filter(
            flow_ticket__action=ActionNum.PENDING,
            hostel__in=hostel,
        )
        column_names = list(TicketShowSerializer.Meta.fields)
        column_names = column_names[: len(column_names) - 1]
        serializer = TicketShowSerializer(grievances, context={"role": role}, many=True)
        response_data = {"columns": column_names, "data": serializer.data}
        return CustomResponse(message=response_data, status=200)


class TicketApprovalView(APIView):  # Api to resolve grievance of student

    permission_classes = [role_permission("WARDEN")]

    def put(self, request, pk):
        user = request.user.id
        role_name, role, hostel = get_user_role(user)
        serializer = TicketApprovalSerializer(data=request.data)
        if serializer.is_valid():
            ticket_id = serializer.validated_data["ticket"]
            action = serializer.validated_data["action"]
            remark = serializer.validated_data["remark"]
            current_approval = TicketApproval.objects.filter(ticket=ticket_id).last()
            if current_approval and current_approval.action != ActionNum.PENDING.value:
                return Response(
                    {"error": "This ticket has already been processed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            update_serializer = TicketApprovalSerializer(
                current_approval,
                data={"action": action, "remark": remark},
                context={"approved_by": user},
                partial=True,
            )
            if update_serializer.is_valid():
                update_serializer.save()
                message = "Grievance closed!"
                return CustomResponse(message=message, status=200)
            else:
                return Response(
                    update_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostelWiseReport(APIView):  # api for reports accessible only to JD

    permission_classes = [role_permission("JD")]

    def get(self, request):
        user = request.user.id
        role_name, role, hostel = get_user_role(user)
        hostel = request.query_params.get("hostel", "")
        if hostel is None:
            return BadResponse(message="No hostel provided")
        hostel = hostel.split(",")
        ticket = Ticket.objects.filter(hostel__in=hostel).order_by("hostel")
        column_names = list(TicketShowSerializer.Meta.fields)
        column_names = column_names[: len(column_names) - 2]
        serializer = TicketShowSerializer(ticket, context={"role": role}, many=True)
        response_data = {"columns": column_names, "data": serializer.data}
        return CustomResponse(message=response_data, status=200)
