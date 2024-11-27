from enum import IntEnum

from django.db import models

from no_auth.models import User

from .manager import BaseManager


class ActionNum(IntEnum):
    PENDING = 0
    RESOLVED = 1
    UNRESOLVED = 2
    ESCALATED = 3
    FORWARD = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def choices_dict(cls):
        return [
            {"value": key.value, "name": key.name}
            for key in cls
            if key.name != "PENDING"
        ]


class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    added_by = models.ForeignKey(
        "no_auth.User",
        related_name="%(class)s_added_by",
        on_delete=models.DO_NOTHING,
        related_query_name="%(class)s_added_by",
        null=True,
    )
    objects = BaseManager()
    unfiltered_objects = models.Manager()

    class Meta:
        abstract = True


class BaseApproveModel(models.Model):
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    approved_by = models.ForeignKey(
        "no_auth.User",
        related_name="%(class)s_added_by",
        on_delete=models.DO_NOTHING,
        related_query_name="%(class)s_added_by",
        null=True,
    )
    objects = BaseManager()
    unfiltered_objects = models.Manager()

    class Meta:
        abstract = True


class Dropdown(BaseModel):
    field = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dropdown_parent",
    )


class LeftPanel(BaseModel):

    role = models.ForeignKey(
        Dropdown, on_delete=models.SET_NULL, related_name="left_panel_roles", null=True
    )
    icon = models.CharField(max_length=50, null=True, blank=False)
    field = models.CharField(max_length=100, null=True, blank=True)
    route = models.CharField(max_length=50, null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, related_name="left_panel_parent", null=True
    )


class Role(BaseModel):
    role = models.ForeignKey(
        Dropdown, on_delete=models.DO_NOTHING, null=True, related_name="role_role"
    )
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, related_name="user_role"
    )
    hostel = models.ForeignKey(
        Dropdown, on_delete=models.DO_NOTHING, null=True, related_name="hostel_role"
    )
