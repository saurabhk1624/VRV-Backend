from rest_framework import serializers
from rest_framework.settings import api_settings

from common.models import Role
from no_auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "date_joined",
            "full_name",
            "username",
            "profile_image",
            "role",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_date_joined(self, obj):
        return obj.date_joined.strftime(api_settings.DATE_FORMAT)

    def get_profile_image(self, obj):
        return obj.profile_image.file.url if obj.profile_image else None

    def get_role(self, obj):
        roles = Role.objects.filter(user=obj.id).distinct()
        role_list = [role.role.field for role in roles]
        return role_list if role_list else None


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
