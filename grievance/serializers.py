from datetime import datetime

from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.settings import api_settings

from common.models import ActionNum, Dropdown, Role
from grievance.models import Ticket, TicketApproval, UploadFile
from no_auth.models import User
from no_auth.serializers import EmployeeSerializer


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["grievance", "issue", "image"]

    def create(self, validated_data):
        ticket = Ticket.objects.create(
            added_by=User.objects.get(id=self.context.get("user")),
            hostel=Dropdown.objects.get(id=self.context.get("hostel")),
            **validated_data,
        )

        return ticket


class TicketImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ["ticket_image", "id"]


class DropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dropdown
        fields = ["field"]


class TicketShowSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()
    hostel = serializers.SerializerMethodField()
    grievance = serializers.SerializerMethodField()
    action_taken = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "hostel",
            "issue",
            "grievance",
            "document",
            "id",
            "action_taken",
        ]

    def get_document(self, obj):
        return obj.image.ticket_image.url if obj.image else None

    def get_hostel(self, obj):
        return obj.hostel.field if obj.hostel else None

    def get_grievance(self, obj):
        return obj.grievance.field if obj.grievance else None

    def get_action_taken(self, obj):
        ticket = TicketApproval.objects.filter(ticket=obj.id).distinct().order_by("id")
        serializer = TicketApprovalSerializer(instance=ticket, many=True)
        return serializer.data


class TicketApprovalSerializer(serializers.ModelSerializer):
    approved_by = EmployeeSerializer(read_only=True)

    class Meta:
        model = TicketApproval
        fields = [
            "ticket",
            "action",
            "remark",
            "approved_by",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        instance.remark = validated_data.get("remark", instance.remark)
        instance.action = validated_data.get("action", instance.action)
        instance.approved_by = User.objects.get(id=self.context.get("approved_by"))
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["action"] = ActionNum(instance.action).name
        data["no_authority_level"] = instance.node.label
        data["approved_by"] = (
            instance.approved_by.first_name + " " + instance.approved_by.last_name
            if instance.approved_by
            else None
        )
        data["action_date"] = (
            instance.updated_at.strftime(api_settings.DATE_FORMAT)
            if instance.approved_by
            else None
        )

        data.pop("updated_at")
        data.pop("ticket")
        data.pop("node")
        return data
